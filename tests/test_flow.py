"""离线组合测试：模型结果为显式测试替身，不作为实跑证据。"""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

VALID_FEATURE = (
    'def due_for_review(terminal_epoch, retention_seconds, now_epoch, hold=False):\n'
    '    if retention_seconds < 0:\n        raise ValueError()\n'
    '    return not hold and now_epoch >= terminal_epoch + retention_seconds\n'
)


class FlowTests(unittest.TestCase):
    def setUp(self):
        from agent_coop import sample
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        base = Path(self.directory.name)
        entry = base / 'unused.js'
        entry.write_text('// never executed', encoding='utf-8')
        hashed = hashlib.sha256(entry.read_bytes()).hexdigest()
        template = Path(sample.__file__).with_name('supervisor-agent.md')
        common = {'adapter': 'codebuddy', 'model': 'fixture', 'executable': str(entry),
                  'entry': str(entry), 'entry_sha256': hashed, 'executable_sha256': hashed,
                  'tools': ['Read', 'Glob', 'Grep'], 'timeout_seconds': 600,
                  'output_limit_bytes': 8388608, 'max_turns': 20}
        self.profiles = {role: dict(common) for role in sample.ROLES}
        self.profiles['implement']['tools'] = common['tools'] + ['Write', 'Edit']
        self.profiles['supervise'].update(
            adapter='kimi', model=None, agent_file=str(template),
            agent_file_sha256=hashlib.sha256(template.read_bytes()).hexdigest(),
        )
        self.root = base / 'run'

    def fixture_invoke(self, profile, prompt, cwd, log_dir, session_id):
        from agent_coop.gates import subject
        from agent_coop.store import Store
        if '-implement-' in session_id:
            source = Path(cwd) / 'workspace' / 'feature.py'
            source.write_text(VALID_FEATURE, encoding='utf-8')
            result = {'artifact': 'workspace/feature.py'}
        else:
            result = {'subject_digest': subject(cwd, Store(cwd).read()),
                      'verdict': 'PASS', 'blocking': []}
        return {'adapter': profile['adapter'], 'actual_model': profile['model'] or 'unknown',
                'session_id': session_id, 'exit_code': 0, 'result': result,
                'raw_text': json.dumps(result), 'test_fixture': True}

    def test_pause_resume_archive_backup_and_cleanup_share_one_state(self):
        from agent_coop.sample import initialize, handlers
        from agent_coop.runner import Runner
        from agent_coop.store import Store
        initialize(self.root, self.profiles)
        store = Store(self.root)
        with patch('agent_coop.runtime.invoke', side_effect=self.fixture_invoke) as invoke:
            Runner(self.root, handlers(self.root)).run(max_steps=2)
            self.assertEqual(invoke.call_count, 1)
            store.pause()
            Runner(self.root, handlers(self.root)).run()
            self.assertEqual(invoke.call_count, 1)
            store.resume()
            Runner(self.root, handlers(self.root)).run()
            state = store.read()
            self.assertEqual(state['phase'], 'complete', state.get('error'))
            self.assertEqual(state['calls_used'], 4)
            self.assertEqual(invoke.call_count, 4)
            Runner(self.root, handlers(self.root)).run()
            self.assertEqual(invoke.call_count, 4)
        self.assertFalse((self.root / 'scratch' / 'fixture.log').exists())
        self.assertTrue((self.root / 'workspace' / 'feature.py').exists())
        backup = json.loads((self.root / 'evidence' / 'backup.json').read_text(encoding='utf-8'))
        self.assertEqual(backup['scope'], 'local_only')
        self.assertTrue((self.root / '.runtime' / 'state.sqlite').exists())

    def test_all_codebuddy_cannot_replace_native_supervisor(self):
        from agent_coop.sample import initialize
        self.profiles['supervise'] = dict(self.profiles['review_a'])
        with self.assertRaisesRegex(ValueError, 'requires kimi'):
            initialize(self.root, self.profiles)
        self.assertFalse(self.root.exists())

    def test_bad_delivery_keeps_receipt_and_budget_without_redispatch(self):
        from agent_coop.sample import initialize, handlers
        from agent_coop.runner import Runner
        from agent_coop.store import Store
        initialize(self.root, self.profiles)
        receipt = {'result': {'artifact': 'wrong'}, 'session_id': 'fixture'}
        with patch('agent_coop.runtime.invoke', return_value=receipt) as invoke:
            Runner(self.root, handlers(self.root)).run()
            state = Store(self.root).read()
            self.assertEqual(state['phase'], 'blocked')
            self.assertEqual(state['calls_used'], 1)
            self.assertTrue((self.root / 'evidence' / 'implement.json').exists())
            try:
                Store(self.root).resume()
            except (ValueError, RuntimeError):
                pass
            Runner(self.root, handlers(self.root)).run()
            self.assertEqual(invoke.call_count, 1)

    def test_verification_failure_blocks_without_verification_evidence(self):
        from agent_coop.sample import initialize, handlers
        from agent_coop.runner import Runner
        from agent_coop.store import Store
        initialize(self.root, self.profiles)

        def bad_implement(profile, prompt, cwd, log_dir, session_id):
            source = Path(cwd) / 'workspace' / 'feature.py'
            source.write_text('def due_for_review(*args, **kwargs): return True\n',
                              encoding='utf-8')
            result = {'artifact': 'workspace/feature.py'}
            return {'adapter': profile['adapter'], 'actual_model': profile['model'] or 'unknown',
                    'session_id': session_id, 'exit_code': 0, 'result': result,
                    'raw_text': json.dumps(result), 'test_fixture': True}

        with patch('agent_coop.runtime.invoke', side_effect=bad_implement):
            Runner(self.root, handlers(self.root)).run()
        state = Store(self.root).read()
        self.assertEqual(state['phase'], 'blocked')
        verify = next(s for s in state['steps'] if s['name'] == 'verify')
        self.assertEqual(verify['status'], 'failed')
        self.assertFalse((self.root / 'evidence' / 'verification.json').exists())

    def test_verification_evidence_write_failure_blocks(self):
        import agent_coop.paths as paths_module
        from agent_coop.sample import initialize, handlers
        from agent_coop.runner import Runner
        from agent_coop.store import Store
        initialize(self.root, self.profiles)
        original = paths_module.write_json

        def flaky_write(path, value):
            if Path(path).name == 'verification.json':
                raise OSError('disk full')
            return original(path, value)

        with patch('agent_coop.runtime.invoke', side_effect=self.fixture_invoke), \
                patch('agent_coop.paths.write_json', side_effect=flaky_write):
            Runner(self.root, handlers(self.root)).run()
        state = Store(self.root).read()
        self.assertEqual(state['phase'], 'blocked')
        verify = next(s for s in state['steps'] if s['name'] == 'verify')
        self.assertEqual(verify['status'], 'failed')
        self.assertFalse((self.root / 'evidence' / 'verification.json').exists())
        self.assertEqual(state['calls_used'], 1)

    def test_review_wrong_verdict_saves_receipt_and_keeps_budget(self):
        from agent_coop.sample import initialize, handlers
        from agent_coop.runner import Runner
        from agent_coop.store import Store
        initialize(self.root, self.profiles)

        def bad_review(profile, prompt, cwd, log_dir, session_id):
            from agent_coop.gates import subject
            from agent_coop.store import Store
            if '-implement-' in session_id:
                source = Path(cwd) / 'workspace' / 'feature.py'
                source.write_text(VALID_FEATURE, encoding='utf-8')
                result = {'artifact': 'workspace/feature.py'}
            else:
                result = {'subject_digest': subject(cwd, Store(cwd).read()),
                          'verdict': 'CHANGES_REQUESTED', 'blocking': ['unresolved']}
            return {'adapter': profile['adapter'], 'actual_model': profile['model'] or 'unknown',
                    'session_id': session_id, 'exit_code': 0, 'result': result,
                    'raw_text': json.dumps(result), 'test_fixture': True}

        with patch('agent_coop.runtime.invoke', side_effect=bad_review):
            Runner(self.root, handlers(self.root)).run()
        state = Store(self.root).read()
        self.assertEqual(state['phase'], 'blocked')
        self.assertEqual(state['calls_used'], 2)
        path = self.root / 'evidence' / 'review_a.json'
        self.assertTrue(path.exists())
        saved = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(saved['result']['verdict'], 'CHANGES_REQUESTED')
