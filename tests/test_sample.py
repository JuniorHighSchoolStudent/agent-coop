"""离线组合证据；显式 test fixture 不代表真实模型票。"""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SampleGateTests(unittest.TestCase):
    def setUp(self):
        from agent_coop import sample
        from agent_coop.gates import implementation_digest, subject
        from agent_coop.paths import create_root
        from agent_coop.paths import digest
        from agent_coop.checks import verifier_digest
        from agent_coop.store import Store
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = create_root(Path(self.directory.name) / 'sample')
        profiles = {role: {'adapter': 'fixture', 'model': 'test'} for role in sample.ROLES}
        config = {'mode': 'test', 'policy': sample.POLICY, 'profiles': profiles,
                  'implementation_digest': implementation_digest()}
        self.store = Store(self.root)
        self.store.initialize(config, list(sample.STEPS))
        source = self.root / 'workspace' / 'feature.py'
        source.write_text('def due_for_review(*args): return False\n', encoding='utf-8')
        current = subject(self.root, self.store.read())
        verification = {'passed': True, 'subject_digest': current,
                        'source_digest': digest(source), 'verifier_digest': verifier_digest()}
        data = {'subject_digest': current,
                'verification': sample.record(self.root, 'verification', verification)}
        for role in sample.ROLES:
            receipt = {'adapter': 'fixture', 'actual_model': 'test', 'session_id': role,
                       'exit_code': 0, 'result': {'subject_digest': current,
                                                'verdict': 'PASS', 'blocking': []}}
            data[role] = sample.record(self.root, role, receipt)
        self.store.update(data=data, calls_used=4)
        self.store.update(data=sample.accept(self.root, self.store.read()))

    def _mutate_evidence(self, name, mutate):
        from agent_coop.paths import digest, write_json
        path = self.root / 'evidence' / f'{name}.json'
        value = json.loads(path.read_text(encoding='utf-8'))
        mutate(value)
        write_json(path, value)
        state = self.store.read()
        state['data'][name]['sha256'] = digest(path)
        return state

    def test_missing_receipt_adapter_is_traceable(self):
        from agent_coop.gates import verify_gate
        state = self._mutate_evidence('implement', lambda v: v.pop('adapter', None))
        with self.assertRaisesRegex(ValueError, 'adapter mismatch for implement'):
            verify_gate(self.root, state)

    def test_review_receipt_without_result_is_traceable(self):
        from agent_coop.gates import verify_gate
        state = self._mutate_evidence('review_a', lambda v: v.pop('result', None))
        with self.assertRaisesRegex(ValueError, 'missing result object'):
            verify_gate(self.root, state)

    def test_wrong_digest_in_review_result_blocks(self):
        from agent_coop.gates import verify_gate
        state = self._mutate_evidence(
            'review_b', lambda v: v['result'].update(subject_digest='0' * 64))
        with self.assertRaisesRegex(ValueError, 'exact subject PASS'):
            verify_gate(self.root, state)

    def test_missing_session_identity_is_traceable(self):
        from agent_coop.gates import verify_gate
        state = self._mutate_evidence('supervise', lambda v: v.update(session_id='unknown'))
        with self.assertRaisesRegex(ValueError, 'missing runtime session identity'):
            verify_gate(self.root, state)

    def test_frozen_config_tamper_is_traceable(self):
        from agent_coop.gates import verify_gate
        state = self.store.read()
        state['config']['model_call_limit'] = 5
        with self.assertRaisesRegex(ValueError, 'config digest changed'):
            verify_gate(self.root, state)

    def test_source_change_invalidates_existing_acceptance(self):
        from agent_coop.gates import verify_gate
        verify_gate(self.root, self.store.read())
        (self.root / 'workspace' / 'feature.py').write_text('# changed\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'candidate changed'):
            verify_gate(self.root, self.store.read())

    def test_changed_review_original_invalidates_acceptance(self):
        from agent_coop.gates import verify_gate
        (self.root / 'evidence' / 'review_a.json').write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence changed'):
            verify_gate(self.root, self.store.read())

    def test_same_actual_session_cannot_count_as_two_reviewers(self):
        from agent_coop.gates import evidence, verify_gate
        from agent_coop.paths import digest, write_json
        state = self.store.read()
        value = evidence(self.root, state, 'review_b')
        value['session_id'] = 'review_a'
        path = self.root / 'evidence' / 'review_b.json'
        write_json(path, value)
        modified = copy.deepcopy(state)
        modified['data']['review_b']['sha256'] = digest(path)
        with self.assertRaisesRegex(ValueError, 'independent'):
            verify_gate(self.root, modified)

    def test_authority_rereads_hold_and_does_not_use_stale_snapshot(self):
        from agent_coop.gates import cleanup_authority
        self.assertFalse(cleanup_authority(self.root)['hold'])
        self.store.update(data={'hold': True})
        self.assertTrue(cleanup_authority(self.root)['hold'])

    def test_version_change_prevents_further_acceptance(self):
        from agent_coop.gates import verify_gate
        from agent_coop.store import canonical_digest
        state = self.store.read()
        state['config']['implementation_digest'] = 'outdated'
        state['config_digest'] = canonical_digest(state['config'])
        with self.assertRaisesRegex(ValueError, 'implementation version changed'):
            verify_gate(self.root, state)

    def test_old_validator_result_cannot_bind_to_new_subject(self):
        from agent_coop.gates import evidence, verified_subject
        state = self.store.read()
        report = evidence(self.root, state, 'verification')
        report['source_digest'] = 'old source'
        with self.assertRaisesRegex(ValueError, 'verified input changed'):
            verified_subject(self.root, state, report)


def _build_profiles(directory):
    """构造四角色合法 profile（executable/entry 为真实占位文件）。"""
    from agent_coop import sample
    entry = Path(directory) / 'unused.js'
    entry.write_text('// never executed', encoding='utf-8')
    hashed = hashlib.sha256(entry.read_bytes()).hexdigest()
    template = Path(sample.__file__).with_name('supervisor-agent.md')
    common = {'adapter': 'codebuddy', 'model': 'fixture', 'executable': str(entry),
              'entry': str(entry), 'entry_sha256': hashed,
              'executable_sha256': hashed, 'tools': ['Read', 'Glob', 'Grep'],
              'timeout_seconds': 600, 'output_limit_bytes': 8388608,
              'max_turns': 20}
    profiles = {role: dict(common) for role in sample.ROLES}
    profiles['implement']['tools'] = common['tools'] + ['Write', 'Edit']
    profiles['supervise'].update(
        adapter='kimi', model=None, agent_file=str(template),
        agent_file_sha256=hashlib.sha256(template.read_bytes()).hexdigest())
    return profiles


FROZEN_INHERIT = ['APPDATA', 'COMSPEC', 'HOME', 'HOMEDRIVE', 'HOMEPATH',
                  'LANG', 'LC_ALL', 'LOCALAPPDATA', 'PATH', 'PATHEXT',
                  'SYSTEMROOT', 'TEMP', 'TMP', 'TZ', 'USERPROFILE', 'WINDIR']
CODEBUDDY_SET = {'CODEBUDDY_DISABLE_AUTO_MEMORY': '1',
                 'CODEBUDDY_CODE_DISABLE_AUTO_MEMORY': '1',
                 'CODEBUDDY_MEMORY_EXTRACTION_ENABLED': '0',
                 'CODEBUDDY_MEMORY_EXTRACTION_DISABLED': '1'}


class SamplePermissionTests(unittest.TestCase):
    def setUp(self):
        from agent_coop import sample
        from agent_coop.store import Store
        self.sample = sample
        self.Store = Store
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.base = Path(self.directory.name)
        self.profiles = _build_profiles(self.base)
        self.root = self.base / 'run'

    def _initialize(self):
        return self.sample.initialize(self.root, self.profiles)

    def _tampered_state(self, mutate):
        from agent_coop.store import canonical_digest
        state = self.Store(self.root).read()
        mutate(state['config'])
        state['config_digest'] = canonical_digest(state['config'])
        return state

    def test_raw_profile_permissions_injection_rejected(self):
        self.profiles['implement']['permissions'] = {'schema': 1}
        with self.assertRaisesRegex(ValueError, 'permissions must not be supplied'):
            self.sample.initialize(self.root, self.profiles)
        self.assertFalse(self.root.exists())

    def test_initialize_deep_copies_profiles(self):
        snapshot = copy.deepcopy(self.profiles)
        self._initialize()
        self.assertEqual(self.profiles, snapshot)
        stored = self.Store(self.root).read()['config']['profiles']['implement']
        stored['permissions']['scope'] = 'tampered'
        self.assertEqual(self.profiles, snapshot)

    def test_initialize_freezes_schema2_and_permissions(self):
        self._initialize()
        config = self.Store(self.root).read()['config']
        self.assertEqual(config['schema'], 2)
        expected_root = self.sample.canonical_path(self.root)
        expected_feature = self.sample.canonical_path(
            self.root / 'workspace' / 'feature.py')
        for role in self.sample.ROLES:
            permissions = config['profiles'][role]['permissions']
            self.assertEqual(permissions['schema'], 1)
            self.assertEqual(permissions['scope'], 'cli_tool_filter_not_os_sandbox')
            self.assertEqual(permissions['root'], expected_root)
            if role == 'implement':
                self.assertEqual(permissions['write_files'], [expected_feature])
            else:
                self.assertEqual(permissions['write_files'], [])
            self.assertEqual(permissions['environment']['inherit'], FROZEN_INHERIT)
            if role == 'supervise':
                self.assertEqual(permissions['environment']['set'], {})
            else:
                self.assertEqual(permissions['environment']['set'], CODEBUDDY_SET)

    def test_config_schema1_rejected_before_reservation(self):
        from unittest.mock import patch
        self._initialize()
        state = self._tampered_state(lambda config: config.update(schema=1))
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'schema 2 required'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_permission_schema_unknown_rejected(self):
        from unittest.mock import patch
        self._initialize()
        state = self._tampered_state(
            lambda config: config['profiles']['implement']['permissions'].update(schema=2))
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'permissions schema must be 1'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_missing_permissions_rejected(self):
        from unittest.mock import patch
        self._initialize()
        state = self._tampered_state(
            lambda config: config['profiles']['implement'].pop('permissions'))
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'missing permissions'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_unexpected_permissions_field_rejected(self):
        from unittest.mock import patch
        self._initialize()
        state = self._tampered_state(
            lambda config: config['profiles']['implement']['permissions'].update(extra='x'))
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'unexpected permissions fields'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_frozen_root_moved_or_noncanonical_rejected(self):
        from unittest.mock import patch
        self._initialize()
        canonical = self.sample.canonical_path(self.root)
        variants = ['X:/moved/root', canonical.replace('/', '\\'), canonical + '/']
        for variant in variants:
            with self.subTest(variant=variant):
                state = self._tampered_state(
                    lambda config, v=variant:
                    config['profiles']['review_a']['permissions'].update(root=v))
                with patch('agent_coop.runtime.invoke') as invoke:
                    with self.assertRaisesRegex(ValueError, 'permissions root moved'):
                        self.sample.dispatch(self.root, state, 'review_a', 'prompt')
                    invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_extra_write_target_rejected(self):
        from unittest.mock import patch
        self._initialize()
        extra = self.sample.canonical_path(self.root / 'scratch' / 'other.py')
        state = self._tampered_state(
            lambda config: config['profiles']['implement']['permissions']
            ['write_files'].append(extra))
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'write_files differ'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_write_target_hardlink_rejected(self):
        from unittest.mock import patch
        self._initialize()
        state = self.Store(self.root).read()
        target = self.root / 'workspace' / 'feature.py'
        target.write_text('existing', encoding='utf-8')
        linked = self.root / 'workspace' / 'linked.py'
        try:
            os.link(target, linked)
        except OSError as exc:
            self.skipTest(f'hard link unavailable: {exc}')
        self.addCleanup(os.unlink, linked)
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'hard links'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    @unittest.skipUnless(sys.platform == 'win32', 'junction 仅 Windows')
    def test_write_target_reparse_rejected(self):
        from unittest.mock import patch
        self._initialize()
        state = self.Store(self.root).read()
        workspace = self.root / 'workspace'
        outside = self.base / 'outside'
        outside.mkdir()
        workspace.rmdir()
        proc = subprocess.run(
            ['cmd', '/c', 'mklink', '/J', str(workspace), str(outside)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            self.skipTest(f'mklink /J 不可用: {proc.stderr.strip()}')
        self.addCleanup(os.rmdir, workspace)
        with patch('agent_coop.runtime.invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'symlink or junction'):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
            invoke.assert_not_called()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 0)

    def test_sample_profile_reaches_invoke_before_popen(self):
        from unittest.mock import patch
        self._initialize()
        state = self.Store(self.root).read()
        with patch('subprocess.Popen',
                   side_effect=RuntimeError('no-start sentinel')) as popen:
            with self.assertRaises(RuntimeError):
                self.sample.dispatch(self.root, state, 'implement', 'prompt')
        popen.assert_called_once()
        self.assertEqual(self.Store(self.root).read()['calls_used'], 1)
