"""固定样例组合；角色来自配置，所有派发经过同一 Runner。"""
import json
import time
import uuid
from pathlib import Path

STEPS = ('implement', 'verify', 'review_a', 'review_b', 'supervise',
         'accept', 'archive', 'backup', 'cleanup_plan', 'cleanup')
ROLES = ('implement', 'review_a', 'review_b', 'supervise')
POLICY = {'id': 'isolated-sample', 'revision': 1, 'retention_seconds': 0,
          'targets': ['scratch/fixture.log'], 'scope': 'local_only'}


def validate_profiles(profiles):
    if not isinstance(profiles, dict) or set(profiles) != set(ROLES):
        raise ValueError('profiles must contain implement, review_a, review_b, supervise')
    from .paths import digest
    for role, profile in profiles.items():
        required_adapter = 'kimi' if role == 'supervise' else 'codebuddy'
        if profile.get('adapter') != required_adapter:
            raise ValueError(f'fixed pilot role requires {required_adapter}: {role}')
        if profile.get('adapter') not in ('codebuddy', 'kimi'):
            raise ValueError('unsupported runtime adapter')
        expected = ['Read', 'Glob', 'Grep']
        if role == 'implement':
            expected += ['Write', 'Edit']
        if set(profile['tools']) != set(expected):
            raise ValueError(f'profile tools differ from role policy: {role}')
        for key in ('executable', 'entry'):
            if not Path(profile[key]).is_absolute() or digest(Path(profile[key])) != profile[key + '_sha256']:
                raise ValueError(f'pinned runtime entry mismatch: {role}/{key}')
        if (profile['timeout_seconds'] != 600 or profile['output_limit_bytes'] != 8388608
                or profile['max_turns'] != 20):
            raise ValueError('profiles must use fixed pilot budgets')
        if profile['adapter'] == 'kimi':
            if profile['model'] is not None or role != 'supervise':
                raise ValueError('native Kimi pilot profile must be read-only supervisor/model null')
            agent_file = Path(profile['agent_file'])
            if not agent_file.is_absolute() or digest(agent_file) != profile['agent_file_sha256']:
                raise ValueError('supervisor agent-file changed')
            template = Path(__file__).with_name('supervisor-agent.md').read_text(encoding='utf-8')
            actual = Path(profile['agent_file']).read_text(encoding='utf-8')
            if actual.strip() != template.strip():
                raise ValueError('supervisor agent-file must match the bundled read-only template')
        elif not isinstance(profile['model'], str) or not profile['model']:
            raise ValueError('explicit model required')


def initialize(path, profiles):
    validate_profiles(profiles)
    from .gates import implementation_digest
    from .paths import create_root
    from .store import Store
    root = create_root(path)
    config = {'schema': 1, 'mode': 'live', 'profiles': profiles, 'policy': POLICY,
              'model_call_limit': 4, 'implementation_digest': implementation_digest()}
    Store(root).initialize(config, list(STEPS))
    (root / 'scratch' / 'fixture.log').write_text('Generated isolated sample only.\n', encoding='utf-8')
    return Store(root).read()


def record(root, name, value):
    from .paths import checked, digest, write_json
    path = checked(root, f'evidence/{name}.json')
    if path.exists():
        raise ValueError(f'evidence already exists: {name}')
    write_json(path, value)
    return {'path': f'evidence/{name}.json', 'sha256': digest(path)}


def dispatch(root, state, role, prompt):
    from .gates import validate_binding
    from .runtime import invoke
    from .paths import checked
    from .store import Store
    validate_binding(state)
    latest = Store(root).read()
    if latest['calls_used'] >= latest['config']['model_call_limit']:
        raise ValueError('model call budget exhausted')
    Store(root).update(calls_used=latest['calls_used'] + 1)
    session = f'coop-{role}-{uuid.uuid4().hex}'
    return invoke(state['config']['profiles'][role], prompt, root,
                  checked(root, f'.runtime/{role}'), session)


def implement(root, state):
    prompt = (
        '实现隔离样例，仅写 workspace/feature.py，不改其他文件。定义纯函数 '
        'due_for_review(terminal_epoch, retention_seconds, now_epoch, hold=False)：'
        '保留期为负抛ValueError；否则hold为真返回False；否则now_epoch达到'
        'terminal_epoch+retention_seconds返回True，其余False。不要运行shell或扩权。'
        '最终只返回严格JSON对象，无markdown：{"artifact":"workspace/feature.py","summary":"..."}。'
    )
    receipt = dispatch(root, state, 'implement', prompt)
    reference = record(root, 'implement', receipt)
    if receipt['result'].get('artifact') != 'workspace/feature.py':
        raise ValueError('implementation artifact missing; receipt: evidence/implement.json')
    return {'implement': reference}


def verify(root, state):
    from .checks import validate_feature
    from .gates import verified_subject
    report = validate_feature(root)
    current = verified_subject(root, state, report)
    report['subject_digest'] = current
    return {'subject_digest': current, 'verification': record(root, 'verification', report)}


def review(root, state, role):
    from .gates import subject, check_verdict, evidence
    current = subject(root, state)
    if current != state['data']['subject_digest']:
        raise ValueError('candidate changed before review')
    evidence(root, state, 'verification')
    sources = 'workspace/feature.py 与 evidence/verification.json'
    if role == 'supervise':
        sources += '、evidence/review_a.json、evidence/review_b.json、evidence/implement.json'
    prompt = (
        f'你是独立只读{role}，非作者。仅阅读 {sources}。核对函数保留期负数抛ValueError、'
        'hold返回False、精确到期边界。监督者另核对两个评审均无阻断、实际会话独立。'
        '仅使用Read/Glob/Grep，不写文件、不shell、不扩权、不启动子agent。'
        f'本次精确候选subject_digest={current}。不得自行改写或猜测digest。'
        '最终只返回一个严格JSON对象，不加代码围栏/前后文字：'
        f'{{"subject_digest":"{current}","verdict":"PASS",'
        '"blocking":[],"summary":"核验依据与限制"}。'
        '如有未决问题改verdict为CHANGES_REQUESTED并填blocking，不能假报PASS。'
    )
    receipt = dispatch(root, state, role, prompt)
    reference = record(root, role, receipt)
    try:
        check_verdict(receipt['result'], current)
    except ValueError as error:
        raise ValueError(f'{error}; receipt: evidence/{role}.json') from error
    return {role: reference}


def accept(root, state):
    from .gates import verify_gate
    current = verify_gate(root, state, require_accept=False)
    receipt = {'accepted': True, 'subject_digest': current, 'terminal_epoch': time.time(),
               'scope': 'isolated_sample', 'os_sandbox': False}
    return {'acceptance': record(root, 'acceptance', receipt)}


def retain(root, state, operation):
    from . import archive
    from .gates import cleanup_authority, evidence, verify_gate
    from .paths import digest, checked
    current = verify_gate(root, state)
    if operation == 'archive':
        entries = ['workspace/feature.py', 'scratch/fixture.log']
        entries += [state['data'][key]['path'] for key in
                    ('implement', 'verification', 'review_a', 'review_b', 'supervise', 'acceptance')]
        archive.create_archive(root, entries, current)
    elif operation == 'backup':
        archive.create_backup(root, evidence(root, state, 'archive'))
    elif operation == 'cleanup_plan':
        archive.plan_cleanup(root, evidence(root, state, 'archive'),
                             evidence(root, state, 'backup'), cleanup_authority(root))
    else:
        archive.apply_cleanup(root, evidence(root, state, 'cleanup_plan'),
                              lambda: cleanup_authority(root))
    filename = operation.replace('_', '-')
    return {operation: {'path': f'evidence/{filename}.json',
                        'sha256': digest(checked(root, f'evidence/{filename}.json'))}}


def handlers(root):
    root = Path(root).absolute()
    result = {'implement': lambda state: implement(root, state),
              'verify': lambda state: verify(root, state),
              'accept': lambda state: accept(root, state)}
    for role in ('review_a', 'review_b', 'supervise'):
        result[role] = lambda state, role=role: review(root, state, role)
    for operation in ('archive', 'backup', 'cleanup_plan', 'cleanup'):
        result[operation] = lambda state, operation=operation: retain(root, state, operation)
    return result
