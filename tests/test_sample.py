"""离线组合证据；显式 test fixture 不代表真实模型票。"""
import copy
import json
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
