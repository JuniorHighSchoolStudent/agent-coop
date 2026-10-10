"""精确候选门禁：正文判断与可信运行身份分别核验。"""
import json
import time
from pathlib import Path


def check_verdict(result, subject_digest):
    if (not isinstance(result, dict)
            or result.get('subject_digest') != subject_digest
            or result.get('verdict') != 'PASS'
            or result.get('blocking') != []):
        raise ValueError('exact subject PASS with empty blocking list required')


def implementation_digest():
    from .paths import digest
    from .store import canonical_digest
    package = Path(__file__).parent
    files = sorted(package.glob('*.py')) + [package / 'supervisor-agent.md']
    return canonical_digest({p.name: digest(p) for p in files})


def validate_binding(state):
    from .store import canonical_digest
    config = state['config']
    if state['config_digest'] != canonical_digest(config):
        raise ValueError('config digest changed')
    if config['implementation_digest'] != implementation_digest():
        raise ValueError('implementation version changed; new reviewed run required')


def subject(root, state):
    from .paths import checked, digest
    from .checks import verifier_digest
    validate_binding(state)
    return subject_digest(digest(checked(root, 'workspace/feature.py')),
                          verifier_digest(), state['config_digest'])


def subject_digest(source_hash, verifier_hash, config_hash):
    from .store import canonical_digest
    return canonical_digest({'source': source_hash, 'verifier': verifier_hash,
                             'config': config_hash})


def evidence(root, state, name):
    from .paths import checked, digest
    reference = state['data'][name]
    path = checked(root, reference['path'])
    try:
        actual = digest(path)
    except OSError as exc:
        raise ValueError(f'evidence missing or unreadable: {name}') from exc
    if actual != reference['sha256']:
        raise ValueError(f'evidence changed: {name}')
    return json.loads(path.read_text(encoding='utf-8'))


def verified_subject(root, state, report):
    verified = subject_digest(report.get('source_digest'), report.get('verifier_digest'),
                              state['config_digest'])
    if verified != subject(root, state):
        raise ValueError('verified input changed before candidate binding')
    return verified


def _receipt_identity(role, receipt, profile, current):
    if not isinstance(receipt, dict):
        raise ValueError(f'receipt must be an object: {role}')
    session = receipt.get('session_id')
    if not session or session == 'unknown':
        raise ValueError(f'missing runtime session identity: {role}')
    if receipt.get('exit_code') != 0:
        raise ValueError(f'non-zero exit code: {role}')
    if receipt.get('adapter') != profile['adapter']:
        raise ValueError(f'adapter mismatch for {role}')
    if profile['model'] is not None and receipt.get('actual_model') != profile['model']:
        raise ValueError(f'actual model differs from pinned profile: {role}')
    if role != 'implement':
        result = receipt.get('result')
        if not isinstance(result, dict):
            raise ValueError(f'review receipt missing result object: {role}')
        check_verdict(result, current)
    return session


def verify_gate(root, state, require_accept=True):
    current = subject(root, state)
    if state['calls_used'] != 4:
        raise ValueError('four recorded model dispatches required')
    if state['data']['subject_digest'] != current:
        raise ValueError('candidate changed after verification')
    report = evidence(root, state, 'verification')
    if verified_subject(root, state, report) != current:
        raise ValueError('verification differs from exact candidate')
    if report.get('passed') is not True or report.get('subject_digest') != current:
        raise ValueError('missing exact verification')
    sessions = []
    for role in ('implement', 'review_a', 'review_b', 'supervise'):
        profile = state['config']['profiles'][role]
        sessions.append(_receipt_identity(
            role, evidence(root, state, role), profile, current))
    if len(set(sessions)) != 4:
        raise ValueError('author, reviewers and supervisor must be independent sessions')
    if require_accept:
        accepted = evidence(root, state, 'acceptance')
        if accepted.get('subject_digest') != current or accepted.get('accepted') is not True:
            raise ValueError('missing exact acceptance')
    return current


def cleanup_authority(root):
    from .store import Store, canonical_digest
    state = Store(root).read()
    current = verify_gate(root, state)
    accepted = evidence(root, state, 'acceptance')
    policy = state['config']['policy']
    return {
        'accepted': True, 'subject_digest': current,
        'config_digest': state['config_digest'], 'policy_digest': canonical_digest(policy),
        'hold': state['data'].get('hold', False),
        'terminal_epoch': accepted['terminal_epoch'],
        'retention_seconds': policy['retention_seconds'], 'now_epoch': time.time(),
    }
