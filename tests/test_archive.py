"""archive/cleanup 归档、备份与清理合同测试（依赖 Store）。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_coop import archive, paths
from agent_coop.store import Store, canonical_digest


def make_link(link_path, target_path):
    """Windows 用 junction，其余用目录符号链接；返回跳过原因或 None。"""
    if sys.platform == 'win32':
        proc = subprocess.run(
            ['cmd', '/c', 'mklink', '/J', str(link_path), str(target_path)],
            capture_output=True, text=True)
        return None if proc.returncode == 0 else f'mklink /J 不可用: {proc.stderr.strip()}'
    try:
        Path(link_path).symlink_to(target_path, target_is_directory=True)
    except OSError as exc:
        return f'symlink 不可用: {exc}'
    return None


def remove_link(path):
    """仅移除 junction/符号链接自身，不递归其目标。"""
    path = Path(path)
    for cleaner in (os.rmdir, os.unlink):
        try:
            cleaner(path)
            return
        except OSError:
            continue

POLICY = {
    'id': 'isolated-sample', 'revision': 1, 'retention_seconds': 0,
    'targets': ['scratch/fixture.log'], 'scope': 'local_only',
}
FIXED_STEPS = ['implement', 'verify', 'review_a', 'review_b', 'supervise',
               'accept', 'archive', 'backup', 'cleanup_plan', 'cleanup']
FIXTURE = 'scratch/fixture.log'
VERIFIER = 'deterministic-validator-v1'
EPOCH = 2_000_000_000


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.root = paths.create_root(self.tmp / 'sample')
        self.store = Store(self.root)
        self.store.initialize({'policy': POLICY}, FIXED_STEPS)
        self.config_digest = self.store.read()['config_digest']
        self.policy_digest = canonical_digest(POLICY)
        self.subject_digest = 'a' * 64

    def make_sources(self):
        feature = self.root / 'workspace' / 'feature.py'
        feature.write_text('def due_for_review():\n    return True\n', encoding='utf-8')
        paths.write_json(self.root / 'evidence' / 'verify.json', {'passed': True})
        return ['workspace/feature.py', 'evidence/verify.json']

    def make_authority(self, **overrides):
        authority = {
            'accepted': True,
            'subject_digest': self.subject_digest,
            'config_digest': self.config_digest,
            'policy_digest': self.policy_digest,
            'hold': False,
            'terminal_epoch': EPOCH,
            'retention_seconds': 0,
            'now_epoch': EPOCH,
        }
        authority.update(overrides)
        return authority

    def make_full_plan(self, **authority_overrides):
        fixture = self.root / FIXTURE
        fixture.write_text('fixture data\n', encoding='utf-8')
        entries = self.make_sources() + [FIXTURE]
        a = archive.create_archive(self.root, entries, self.subject_digest)
        b = archive.create_backup(self.root, a)
        plan = archive.plan_cleanup(
            self.root, a, b, self.make_authority(**authority_overrides))
        return plan, a, b, fixture

    def read_evidence(self, name):
        return json.loads((self.root / 'evidence' / name).read_text(encoding='utf-8'))

    def test_create_archive_receipt_copies_and_persists(self):
        sources = self.make_sources()
        receipt = archive.create_archive(self.root, sources, self.subject_digest)
        self.assertEqual(receipt['subject_digest'], self.subject_digest)
        self.assertEqual(receipt['policy_id'], POLICY['id'])
        self.assertEqual(receipt['policy_revision'], POLICY['revision'])
        self.assertEqual(receipt['policy_digest'], self.policy_digest)
        self.assertEqual(receipt['verifier'], VERIFIER)
        self.assertEqual(receipt['permissions'], 'local_user')
        self.assertEqual(receipt['unresolved_obligations'], [])
        self.assertIsInstance(receipt['verified_epoch'], int)
        self.assertEqual({f['source'] for f in receipt['files']}, set(sources))
        for entry in receipt['files']:
            source = self.root / entry['source']
            self.assertEqual(entry['size'], source.stat().st_size)
            self.assertEqual(entry['sha256'], paths.digest(source))
            target = self.root / entry['target']
            self.assertTrue(target.is_file())
            self.assertEqual(target.read_bytes(), source.read_bytes())
        self.assertEqual(self.read_evidence('archive.json'), receipt)

    def test_create_archive_rejects_runtime_db_and_duplicate(self):
        sources = self.make_sources()
        cases = (('runtime_db', ['.runtime/state.sqlite']),
                 ('duplicate', [sources[0], sources[0]]))
        for name, entries in cases:
            with self.subTest(rejection=name), self.assertRaises(ValueError):
                archive.create_archive(self.root, entries, self.subject_digest)

    def test_create_archive_rejects_symlink_entry(self):
        outside = self.tmp / 'outside.txt'
        outside.write_text('x', encoding='utf-8')
        link = self.root / 'workspace' / 'link.txt'
        try:
            link.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f'symlink 不可用: {exc}')
        with self.assertRaises(ValueError):
            archive.create_archive(
                self.root, ['workspace/link.txt'], self.subject_digest)

    def test_create_archive_idempotent_and_rejects_changes(self):
        sources = self.make_sources()
        first = archive.create_archive(self.root, sources, self.subject_digest)
        target = self.root / first['files'][0]['target']
        before = target.read_bytes()
        self.assertEqual(
            archive.create_archive(self.root, sources, self.subject_digest), first)
        self.assertEqual(target.read_bytes(), before)  # 旧目标 bytes 不变
        (self.root / sources[0]).write_text('CHANGED\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            archive.create_archive(self.root, sources, self.subject_digest)

    def test_create_backup_local_only_persisted_and_idempotent(self):
        a = archive.create_archive(self.root, self.make_sources(), self.subject_digest)
        first = archive.create_backup(self.root, a)
        self.assertEqual(first['scope'], 'local_only')
        self.assertEqual(first['subject_digest'], self.subject_digest)
        self.assertEqual(first['policy_digest'], self.policy_digest)
        self.assertEqual(self.read_evidence('backup.json'), first)
        for entry in first['files']:
            target = self.root / entry['target']
            self.assertEqual(entry['sha256'], paths.digest(target))
            self.assertEqual(target.read_bytes(),
                             (self.root / entry['source']).read_bytes())
        backup_target = self.root / first['files'][0]['target']
        before = backup_target.read_bytes()
        self.assertEqual(archive.create_backup(self.root, a), first)
        self.assertEqual(backup_target.read_bytes(), before)  # 旧目标 bytes 不变
        (self.root / a['files'][0]['target']).write_bytes(b'tampered')
        with self.assertRaises(ValueError):
            archive.create_backup(self.root, a)

    def test_plan_cleanup_fixed_target_and_persisted(self):
        plan, a, b, fixture = self.make_full_plan()
        self.assertEqual(plan['source'], FIXTURE)
        self.assertEqual(plan['subject_digest'], self.subject_digest)
        self.assertEqual(plan['config_digest'], self.config_digest)
        self.assertEqual(plan['policy_digest'], self.policy_digest)
        self.assertEqual(plan['terminal_epoch'], EPOCH)
        self.assertEqual(plan['retention_seconds'], 0)
        self.assertRegex(plan['plan_digest'], '^[0-9a-f]{64}$')
        self.assertEqual(self.read_evidence('cleanup-plan.json'), plan)

    def test_plan_cleanup_rejects_invalid_authority(self):
        a = archive.create_archive(self.root, self.make_sources(), self.subject_digest)
        b = archive.create_backup(self.root, a)
        good = self.make_authority()
        cases = []
        for field in good:
            bad = dict(good)
            del bad[field]
            cases.append((f'missing_{field}', bad))
        cases += [('hold', {**good, 'hold': True}),
                  ('not_accepted', {**good, 'accepted': False}),
                  ('not_due', {**good, 'now_epoch': 1_000_000_000,
                               'terminal_epoch': EPOCH}),
                  ('wrong_policy', {**good, 'policy_digest': 'z' * 64})]
        for name, authority in cases:
            with self.subTest(authority=name), self.assertRaises(ValueError):
                archive.plan_cleanup(self.root, a, b, authority)

    def test_plan_cleanup_rejects_fixture_not_backed_up(self):
        fixture = self.root / FIXTURE
        fixture.write_text('fixture data\n', encoding='utf-8')
        a = archive.create_archive(
            self.root, self.make_sources() + [FIXTURE], self.subject_digest)
        b = archive.create_backup(self.root, a)
        partial = dict(b)
        partial['files'] = [f for f in b['files']
                            if not f['source'].endswith(FIXTURE)]
        paths.write_json(self.root / 'evidence' / 'backup.json', partial)
        with self.assertRaises(ValueError):
            archive.plan_cleanup(self.root, a, partial, self.make_authority())
        self.assertTrue(fixture.exists())

    def test_apply_cleanup_deletes_only_fixture_and_persists(self):
        plan, a, b, fixture = self.make_full_plan()
        receipt = archive.apply_cleanup(self.root, plan, self.make_authority)
        self.assertFalse(fixture.exists())
        self.assertFalse(receipt['failed'])
        self.assertEqual(receipt['results'][0]['status'], 'deleted')
        self.assertEqual(self.read_evidence('cleanup.json'), receipt)
        for path in ('workspace/feature.py', 'evidence/verify.json',
                     '.runtime/state.sqlite', 'evidence/archive.json',
                     'evidence/backup.json'):
            self.assertTrue((self.root / path).exists(), path)

    def test_apply_cleanup_allows_changed_now_if_still_due(self):
        plan, a, b, fixture = self.make_full_plan(
            now_epoch=1_000_000_000, terminal_epoch=1_000_000_000)
        authorize = lambda: self.make_authority(
            now_epoch=1_000_000_100, terminal_epoch=1_000_000_000)
        archive.apply_cleanup(self.root, plan, authorize)
        self.assertFalse(fixture.exists())

    def test_apply_cleanup_rejects_authority_variations(self):
        variations = {
            'hold': {'hold': True},
            'not_accepted': {'accepted': False},
            'not_due': {'now_epoch': 1_000_000_000, 'terminal_epoch': EPOCH},
            'changed_subject': {'subject_digest': 'z' * 64},
            'changed_config': {'config_digest': 'z' * 64},
            'changed_policy': {'policy_digest': 'z' * 64},
        }
        for name, overrides in variations.items():
            with self.subTest(rejection=name):
                plan, a, b, fixture = self.make_full_plan()
                with self.assertRaises(ValueError):
                    archive.apply_cleanup(
                        self.root, plan, lambda o=overrides: self.make_authority(**o))
                self.assertTrue(fixture.exists(), name)

    def test_apply_cleanup_rejects_source_and_plan_changes(self):
        cases = [
            ('changed_source',
             lambda r, p, a, b, f: f.write_text('different\n', encoding='utf-8')),
            ('tampered_plan',
             lambda r, p, a, b, f: p.update(subject_digest='x' * 64)),
            ('unpersisted_plan',
             lambda r, p, a, b, f: (r / 'evidence' / 'cleanup-plan.json').unlink()),
        ]
        for name, mutate in cases:
            with self.subTest(rejection=name):
                plan, a, b, fixture = self.make_full_plan()
                mutate(self.root, plan, a, b, fixture)
                with self.assertRaises(ValueError):
                    archive.apply_cleanup(self.root, plan, self.make_authority)
                self.assertTrue(fixture.exists(), name)

    def test_apply_cleanup_rejects_changed_archive_or_backup(self):
        for manifest_name in ('archive', 'backup'):
            with self.subTest(manifest=manifest_name):
                plan, a, b, fixture = self.make_full_plan()
                receipt = a if manifest_name == 'archive' else b
                target = self.root / receipt['files'][0]['target']
                original = target.read_bytes()
                try:
                    target.write_bytes(b'tampered\n')
                    with self.assertRaises(ValueError):
                        archive.apply_cleanup(self.root, plan, self.make_authority)
                    self.assertTrue(fixture.exists(), manifest_name)
                finally:
                    target.write_bytes(original)

    def test_apply_cleanup_permission_error_keeps_failure_receipt(self):
        plan, a, b, fixture = self.make_full_plan()
        if os.name == 'nt':
            os.chmod(fixture, 0o444)  # 只读属性 -> DeleteFileW 拒绝
            self.addCleanup(os.chmod, fixture, 0o666)
        else:
            if hasattr(os, 'geteuid') and os.geteuid() == 0:
                self.skipTest('running as root; permission-denied path not exercisable')
            os.chmod(fixture.parent, 0o500)  # 去掉父目录写权限 -> unlink 拒绝
            self.addCleanup(os.chmod, fixture.parent, 0o700)
        receipt = archive.apply_cleanup(self.root, plan, self.make_authority)
        self.assertTrue(fixture.exists())
        self.assertTrue(receipt['failed'])
        self.assertEqual(receipt['results'][0]['status'], 'failed')
        self.assertTrue(receipt['results'][0]['error'])
        self.assertEqual(self.read_evidence('cleanup.json'), receipt)

    def test_create_archive_rejects_changed_target_content(self):
        sources = self.make_sources()
        a = archive.create_archive(self.root, sources, self.subject_digest)
        target = self.root / a['files'][0]['target']
        target.write_bytes(b'tampered\n')
        with self.assertRaises(ValueError):
            archive.create_archive(self.root, sources, self.subject_digest)
        self.assertEqual(target.read_bytes(), b'tampered\n')  # 不覆写被改内容

    def test_create_backup_rejects_changed_backup_target_content(self):
        a = archive.create_archive(self.root, self.make_sources(), self.subject_digest)
        b = archive.create_backup(self.root, a)
        target = self.root / b['files'][0]['target']
        target.write_bytes(b'tampered\n')
        with self.assertRaises(ValueError):
            archive.create_backup(self.root, a)
        self.assertEqual(target.read_bytes(), b'tampered\n')

    def test_create_archive_rejects_existing_target_without_receipt(self):
        sources = self.make_sources()
        leftover = self.root / 'archives' / self.subject_digest / sources[0]
        leftover.parent.mkdir(parents=True, exist_ok=True)
        leftover.write_text('leftover\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            archive.create_archive(self.root, sources, self.subject_digest)
        self.assertEqual(leftover.read_text(encoding='utf-8'), 'leftover\n')

    def test_create_archive_rejects_prebuilt_archives_junction(self):
        sources = self.make_sources()
        outside = self.tmp / 'outside'
        outside.mkdir()
        junction = self.root / 'archives' / self.subject_digest
        junction.parent.mkdir(parents=True, exist_ok=True)
        reason = make_link(junction, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, junction)
        with self.assertRaises(ValueError):
            archive.create_archive(self.root, sources, self.subject_digest)
        self.assertEqual(list(outside.iterdir()), [])

    def test_create_backup_rejects_prebuilt_backups_junction(self):
        a = archive.create_archive(self.root, self.make_sources(), self.subject_digest)
        outside = self.tmp / 'outside'
        outside.mkdir()
        junction = self.root / 'backups' / self.subject_digest
        junction.parent.mkdir(parents=True, exist_ok=True)
        reason = make_link(junction, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, junction)
        with self.assertRaises(ValueError):
            archive.create_backup(self.root, a)
        self.assertEqual(list(outside.iterdir()), [])

    def test_apply_cleanup_rejects_junctioned_archive_parent(self):
        plan, a, b, fixture = self.make_full_plan()
        target = self.root / a['files'][0]['target']
        original = target.read_bytes()
        parent = target.parent
        target.unlink()
        parent.rmdir()
        outside = self.tmp / 'outside'
        outside.mkdir()
        (outside / target.name).write_bytes(original)
        reason = make_link(parent, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, parent)
        with self.assertRaises(ValueError):
            archive.apply_cleanup(self.root, plan, self.make_authority)
        self.assertTrue(fixture.exists())

    def test_apply_cleanup_rejects_junctioned_backup_parent(self):
        plan, a, b, fixture = self.make_full_plan()
        target = self.root / b['files'][0]['target']
        original = target.read_bytes()
        parent = target.parent
        target.unlink()
        parent.rmdir()
        outside = self.tmp / 'outside'
        outside.mkdir()
        (outside / target.name).write_bytes(original)
        reason = make_link(parent, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, parent)
        with self.assertRaises(ValueError):
            archive.apply_cleanup(self.root, plan, self.make_authority)
        self.assertTrue(fixture.exists())

    def test_apply_cleanup_rejects_rebound_source(self):
        plan, a, b, fixture = self.make_full_plan()
        source = self.root / 'workspace' / 'feature.py'
        tampered = dict(plan)
        tampered['source'] = 'workspace/feature.py'
        tampered['source_sha256'] = paths.digest(source)
        body = {k: v for k, v in tampered.items() if k != 'plan_digest'}
        tampered['plan_digest'] = canonical_digest(body)
        paths.write_json(self.root / 'evidence' / 'cleanup-plan.json', tampered)
        with self.assertRaises(ValueError):
            archive.apply_cleanup(self.root, tampered, self.make_authority)
        self.assertTrue(source.exists())
        self.assertTrue(fixture.exists())

    def test_plan_cleanup_rejects_subject_mismatch(self):
        fixture = self.root / FIXTURE
        fixture.write_text('fixture data\n', encoding='utf-8')
        a = archive.create_archive(
            self.root, self.make_sources() + [FIXTURE], self.subject_digest)
        b = archive.create_backup(self.root, a)
        with self.assertRaises(ValueError):
            archive.plan_cleanup(
                self.root, a, b, self.make_authority(subject_digest='b' * 64))

    def test_apply_cleanup_rejects_receipt_metadata_change(self):
        for name in ('archive', 'backup'):
            with self.subTest(receipt=name):
                plan, a, b, fixture = self.make_full_plan()
                path = self.root / 'evidence' / f'{name}.json'
                original = path.read_bytes()
                try:
                    receipt = json.loads(original.decode('utf-8'))
                    receipt['subject_digest'] = 'c' * 64
                    paths.write_json(path, receipt)
                    with self.assertRaises(ValueError):
                        archive.apply_cleanup(self.root, plan, self.make_authority)
                    self.assertTrue(fixture.exists(), name)
                finally:
                    path.write_bytes(original)

    def test_plan_cleanup_rejects_corrupt_target(self):
        for manifest_name in ('archive', 'backup'):
            with self.subTest(manifest=manifest_name):
                fixture = self.root / FIXTURE
                fixture.write_text('fixture data\n', encoding='utf-8')
                a = archive.create_archive(
                    self.root, self.make_sources() + [FIXTURE], self.subject_digest)
                b = archive.create_backup(self.root, a)
                receipt = a if manifest_name == 'archive' else b
                target = self.root / receipt['files'][0]['target']
                original = target.read_bytes()
                try:
                    target.write_bytes(b'corrupt\n')
                    with self.assertRaises(ValueError):
                        archive.plan_cleanup(self.root, a, b, self.make_authority())
                finally:
                    target.write_bytes(original)

    def test_apply_cleanup_source_changed_by_authorize_not_deleted(self):
        plan, a, b, fixture = self.make_full_plan()
        calls = []

        def authorize():
            calls.append(1)
            if len(calls) == 2:
                fixture.write_text('changed by authorize\n', encoding='utf-8')
            return self.make_authority()

        receipt = archive.apply_cleanup(self.root, plan, authorize)
        self.assertTrue(fixture.exists())
        self.assertEqual(fixture.read_text(encoding='utf-8'),
                         'changed by authorize\n')
        self.assertTrue(receipt['failed'])
        self.assertEqual(receipt['results'][0]['status'], 'failed')
        self.assertEqual(self.read_evidence('cleanup.json'), receipt)


if __name__ == '__main__':
    unittest.main()
