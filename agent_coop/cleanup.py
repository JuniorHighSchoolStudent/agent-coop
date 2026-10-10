"""隔离样例的清理计划与授权删除。

负责 plan（固定 scratch 清单 + 稳定字段 + plan_digest）、authority 严格核验与
逐对象删除；archive.py 的 plan_cleanup/apply_cleanup 仅薄转发至此，不复制规则。
"""
import json
import math
import time
from pathlib import Path

FIXED_POLICY = {'id': 'isolated-sample', 'revision': 1, 'retention_seconds': 0,
                'targets': ['scratch/fixture.log'], 'scope': 'local_only'}
VERIFIER = 'deterministic-validator-v1'
FIXTURE = 'scratch/fixture.log'


def read_store(root):
    from .store import Store
    return Store(root).read()


def validate_policy(config, config_digest):
    from .store import canonical_digest
    if canonical_digest(config) != config_digest:
        raise ValueError('config digest mismatch')
    policy = config.get('policy')
    if policy != FIXED_POLICY:
        raise ValueError('non-sample policy')
    return policy


def validate_subject_digest(subject_digest):
    if not isinstance(subject_digest, str) or len(subject_digest) != 64:
        raise ValueError('invalid subject_digest')
    try:
        int(subject_digest, 16)
    except ValueError:
        raise ValueError('invalid subject_digest')


def read_evidence(root, name):
    from .paths import checked
    path = checked(root, f'evidence/{name}')
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except OSError as exc:
        raise ValueError(f'evidence missing: {name}') from exc


def _finite(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def validate_authority(state, authority):
    from .store import canonical_digest
    required = ('accepted', 'subject_digest', 'config_digest', 'policy_digest',
                'hold', 'terminal_epoch', 'retention_seconds', 'now_epoch')
    if not isinstance(authority, dict) or set(required) - set(authority):
        raise ValueError('authority missing fields')
    if authority['accepted'] is not True:
        raise ValueError('not accepted')
    if authority['hold'] is not False:
        raise ValueError('hold active')
    if authority['config_digest'] != state['config_digest']:
        raise ValueError('config digest changed')
    policy = state['config']['policy']
    if policy != FIXED_POLICY:
        raise ValueError('non-sample policy')
    if authority['policy_digest'] != canonical_digest(policy):
        raise ValueError('policy digest changed')
    if authority['retention_seconds'] != 0:
        raise ValueError('retention must be zero')
    if not _finite(authority['terminal_epoch']) or not _finite(authority['now_epoch']):
        raise ValueError('non-finite epoch')
    if authority['now_epoch'] < authority['terminal_epoch'] + authority['retention_seconds']:
        raise ValueError('not yet due')
    return authority


def _fixture_manifest_entry(archive_receipt, backup_receipt, source_hash):
    archive_entry = next((e for e in archive_receipt.get('files', [])
                          if e.get('source') == FIXTURE), None)
    if archive_entry is None:
        raise ValueError('fixture not archived')
    if archive_entry.get('sha256') != source_hash:
        raise ValueError('archive fixture hash differs from source')
    backup_entry = next((e for e in backup_receipt.get('files', [])
                         if e.get('source') == archive_entry.get('target')), None)
    if backup_entry is None:
        raise ValueError('fixture not backed up')
    if backup_entry.get('sha256') != source_hash:
        raise ValueError('backup fixture hash differs from source')
    return archive_entry, backup_entry


def plan_digest(plan):
    from .store import canonical_digest
    body = {key: value for key, value in plan.items() if key != 'plan_digest'}
    return canonical_digest(body)


def plan_cleanup(root, archive_receipt, backup_receipt, authority):
    from .paths import checked, digest, write_json
    state = read_store(root)
    validate_policy(state['config'], state['config_digest'])
    validate_authority(state, authority)

    if read_evidence(root, 'archive.json') != archive_receipt:
        raise ValueError('archive receipt not persisted')
    if read_evidence(root, 'backup.json') != backup_receipt:
        raise ValueError('backup receipt not persisted')

    fixture = checked(root, FIXTURE)
    if not fixture.is_file():
        raise ValueError('fixture missing')
    source_hash = digest(fixture)
    _fixture_manifest_entry(archive_receipt, backup_receipt, source_hash)

    plan = {
        'source': FIXTURE,
        'source_sha256': source_hash,
        'subject_digest': authority['subject_digest'],
        'config_digest': authority['config_digest'],
        'policy_digest': authority['policy_digest'],
        'terminal_epoch': authority['terminal_epoch'],
        'retention_seconds': 0,
        'archive_files': archive_receipt['files'],
        'backup_files': backup_receipt['files'],
    }
    plan['plan_digest'] = plan_digest(plan)
    write_json(checked(root, 'evidence/cleanup-plan.json'), plan)
    return plan


def _verify_manifest_targets(root, files):
    from .paths import digest
    for entry in files:
        target = Path(root) / entry['target']
        if not target.is_file():
            raise ValueError(f'target missing: {entry["target"]}')
        if target.stat().st_size != entry['size'] or digest(target) != entry['sha256']:
            raise ValueError(f'target changed: {entry["target"]}')


def _stable_fields(plan, authority):
    for key in ('subject_digest', 'config_digest', 'policy_digest',
                'terminal_epoch', 'retention_seconds'):
        if authority[key] != plan[key]:
            raise ValueError(f'stable field changed: {key}')


def _cleanup_receipt(plan, status, error):
    return {
        'source': plan['source'],
        'subject_digest': plan['subject_digest'],
        'policy_digest': plan['policy_digest'],
        'failed': status == 'failed',
        'results': [{'source': plan['source'], 'status': status, 'error': error}],
        'verified_epoch': int(time.time()),
    }


def apply_cleanup(root, plan, authorize):
    from .paths import checked, digest, write_json
    state = read_store(root)
    validate_policy(state['config'], state['config_digest'])

    if read_evidence(root, 'cleanup-plan.json') != plan:
        raise ValueError('plan not persisted or tampered')
    if plan_digest(plan) != plan.get('plan_digest'):
        raise ValueError('plan digest mismatch')

    authority = validate_authority(state, authorize())
    _stable_fields(plan, authority)

    fixture = checked(root, plan['source'])
    if not fixture.is_file() or digest(fixture) != plan['source_sha256']:
        raise ValueError('source changed')

    if read_evidence(root, 'archive.json').get('files') != plan['archive_files']:
        raise ValueError('archive receipt changed')
    if read_evidence(root, 'backup.json').get('files') != plan['backup_files']:
        raise ValueError('backup receipt changed')
    _verify_manifest_targets(root, plan['archive_files'])
    _verify_manifest_targets(root, plan['backup_files'])

    receipt_path = checked(root, 'evidence/cleanup.json')
    write_json(receipt_path, {'source': plan['source'], 'intent': 'cleanup'})

    fixture = checked(root, plan['source'])
    if not fixture.is_file() or digest(fixture) != plan['source_sha256']:
        raise ValueError('source changed before deletion')
    authority = validate_authority(state, authorize())
    _stable_fields(plan, authority)

    try:
        fixture.unlink()
        receipt = _cleanup_receipt(plan, 'deleted', None)
    except OSError as exc:
        receipt = _cleanup_receipt(plan, 'failed', str(exc))

    write_json(receipt_path, receipt)
    return receipt
