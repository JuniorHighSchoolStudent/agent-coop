"""隔离样例的归档复制、清单、恢复验证与本机备份。

负责 create_archive（白名单复制 + 逐文件 hash 读回 + 独立临时恢复验证）与
create_backup（本机副本 local_only）。plan_cleanup/apply_cleanup 薄转发至
cleanup.py，不在此复制清理规则。
"""
import json
import tempfile
import time
from pathlib import Path, PurePosixPath

from .cleanup import (VERIFIER, read_evidence, read_store, validate_policy,
                      validate_subject_digest)
from .paths import checked, digest, write_json
from .store import canonical_digest


def _copy_verified(source, target, size, sha256):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    if source.stat().st_size != size or digest(source) != sha256:
        raise ValueError(f'source changed during copy: {source}')
    if target.stat().st_size != size or digest(target) != sha256:
        raise ValueError(f'target mismatch after copy: {target}')
    with tempfile.TemporaryDirectory(prefix='agent-coop-restore-') as restore:
        restored = Path(restore) / target.name
        restored.write_bytes(target.read_bytes())
        if restored.stat().st_size != size or digest(restored) != sha256:
            raise ValueError(f'restore verification failed: {target}')


def _validate_entries(root, entries):
    if not isinstance(entries, (list, tuple)) or not entries:
        raise ValueError('entries must be a non-empty list')
    validated = []
    seen = set()
    for entry in entries:
        text = str(entry)
        path = checked(root, text)
        top = PurePosixPath(text.replace('\\', '/')).parts[0]
        if top not in ('workspace', 'evidence', 'scratch'):
            raise ValueError(f'entry outside whitelist: {text}')
        if not path.is_file():
            raise ValueError(f'entry is not a file: {text}')
        if text in seen:
            raise ValueError(f'duplicate entry: {text}')
        seen.add(text)
        validated.append(text)
    return validated


def _existing_receipt(root, name, receipt):
    path = checked(root, f'evidence/{name}')
    stable = {k: v for k, v in receipt.items() if k != 'verified_epoch'}
    if not path.exists():
        return None
    existing = json.loads(path.read_text(encoding='utf-8'))
    if {k: v for k, v in existing.items() if k != 'verified_epoch'} != stable:
        raise ValueError(f'{name} differs from existing evidence')
    return existing


def _verify_target(root, entry):
    target = checked(root, entry['target'])
    if not target.is_file():
        raise ValueError(f'target missing: {entry["target"]}')
    if target.stat().st_size != entry['size'] or digest(target) != entry['sha256']:
        raise ValueError(f'target changed: {entry["target"]}')
    return target


def _receipt(subject_digest, policy, files):
    return {
        'subject_digest': subject_digest,
        'policy_id': policy['id'],
        'policy_revision': policy['revision'],
        'policy_digest': canonical_digest(policy),
        'verifier': VERIFIER,
        'verified_epoch': int(time.time()),
        'permissions': 'local_user',
        'unresolved_obligations': [],
        'files': files,
    }


def create_archive(root, entries, subject_digest):
    state = read_store(root)
    policy = validate_policy(state['config'], state['config_digest'])
    validate_subject_digest(subject_digest)

    files = []
    for relative in _validate_entries(root, entries):
        source = checked(root, relative)
        files.append({'source': relative,
                      'target': f'archives/{subject_digest}/{relative}',
                      'size': source.stat().st_size, 'sha256': digest(source)})

    receipt = _receipt(subject_digest, policy, files)
    existing = _existing_receipt(root, 'archive.json', receipt)
    if existing is not None:
        for entry in files:
            _verify_target(root, entry)
        return existing
    for entry in files:
        if checked(root, entry['target']).exists():
            raise ValueError(f'target already exists without receipt: {entry["target"]}')
    for entry in files:
        _copy_verified(checked(root, entry['source']),
                       checked(root, entry['target']), entry['size'], entry['sha256'])
    write_json(checked(root, 'evidence/archive.json'), receipt)
    return receipt


def create_backup(root, archive_receipt):
    state = read_store(root)
    policy = validate_policy(state['config'], state['config_digest'])

    if read_evidence(root, 'archive.json') != archive_receipt:
        raise ValueError('archive receipt not persisted')
    subject_digest = archive_receipt['subject_digest']
    validate_subject_digest(subject_digest)

    files = []
    for entry in archive_receipt['files']:
        archive_target_rel = entry['target']
        archive_target = checked(root, archive_target_rel)
        if not archive_target.is_file():
            raise ValueError(f'archive target missing: {archive_target_rel}')
        if archive_target.stat().st_size != entry['size'] or digest(archive_target) != entry['sha256']:
            raise ValueError(f'archive target changed: {archive_target_rel}')
        files.append({'source': archive_target_rel,
                      'target': f'backups/{subject_digest}/{entry["source"]}',
                      'size': entry['size'], 'sha256': entry['sha256']})

    receipt = _receipt(subject_digest, policy, files)
    receipt['scope'] = 'local_only'
    existing = _existing_receipt(root, 'backup.json', receipt)
    if existing is not None:
        for entry in files:
            _verify_target(root, entry)
        return existing
    for entry in files:
        if checked(root, entry['target']).exists():
            raise ValueError(f'target already exists without receipt: {entry["target"]}')
    for entry in files:
        _copy_verified(checked(root, entry['source']),
                       checked(root, entry['target']), entry['size'], entry['sha256'])
    write_json(checked(root, 'evidence/backup.json'), receipt)
    return receipt


def plan_cleanup(root, archive_receipt, backup_receipt, authority):
    from .cleanup import plan_cleanup as _plan_cleanup
    return _plan_cleanup(root, archive_receipt, backup_receipt, authority)


def apply_cleanup(root, plan, authorize):
    from .cleanup import apply_cleanup as _apply_cleanup
    return _apply_cleanup(root, plan, authorize)
