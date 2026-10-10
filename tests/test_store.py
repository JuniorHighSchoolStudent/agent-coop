"""Store 持久状态、单写权威与发布投影的合同测试。

断言的是 SQLite 权威的对外行为；发布投影假定写在 root/STATUS 与
root/state.json（具体路径由集成者统一收敛）。
"""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path


def _expected_digest(value):
    text = json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _make_store(root):
    from agent_coop.store import Store
    return Store(root)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / 'sample'
        (self.root / '.runtime').mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_initialize_sets_initial_fields(self):
        from agent_coop.store import canonical_digest
        store = _make_store(self.root)
        config = {'policy': 'isolated-sample', 'retention_seconds': 0}
        store.initialize(config, ['implement', 'verify'])
        state = store.read()
        self.assertEqual(state['schema'], 1)
        self.assertEqual(state['phase'], 'ready')
        self.assertFalse(state['paused'])
        self.assertIsNone(state['current_step'])
        self.assertEqual(state['data'], {})
        self.assertIsNone(state['error'])
        self.assertEqual(state['calls_used'], 0)
        self.assertEqual(state['config'], config)
        self.assertEqual(state['config_digest'], canonical_digest(config))
        self.assertEqual(state['steps'], [
            {'name': 'implement', 'status': 'pending'},
            {'name': 'verify', 'status': 'pending'},
        ])
        self.assertIsInstance(state['revision'], int)

    def test_initialize_refuses_to_reset_existing_db(self):
        store = _make_store(self.root)
        store.initialize({'a': 1}, ['implement'])
        store.update(calls_used=5)
        with self.assertRaises(Exception):
            store.initialize({'b': 2}, ['other'])
        state = store.read()
        self.assertEqual(state['calls_used'], 5)
        self.assertEqual(state['config'], {'a': 1})

    def test_initialize_validates_inputs(self):
        store = _make_store(self.root)
        with self.assertRaises(TypeError):
            store.initialize('not-a-dict', ['a'])
        with self.assertRaises(ValueError):
            store.initialize({}, [])
        with self.assertRaises(ValueError):
            store.initialize({}, ['a', 'a'])
        with self.assertRaises(ValueError):
            store.initialize({}, ['', 'b'])

    def test_canonical_digest_is_sorted_compact_utf8_sha256(self):
        from agent_coop.store import canonical_digest
        value = {'b': 1, 'a': '你好'}
        self.assertEqual(canonical_digest(value), _expected_digest(value))
        self.assertEqual(canonical_digest({'a': '你好', 'b': 1}),
                         _expected_digest(value))
        ascii_escaped = json.dumps(value, sort_keys=True,
                                   separators=(',', ':')).encode('utf-8')
        self.assertNotEqual(canonical_digest(value),
                            hashlib.sha256(ascii_escaped).hexdigest())

    def test_update_merges_data_field(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.update(data={'hold': True})
        self.assertEqual(store.read()['data'], {'hold': True})
        store.update(data={'extra': 1})
        self.assertEqual(store.read()['data'], {'hold': True, 'extra': 1})

    def test_update_increments_revision(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        first = store.read()['revision']
        store.update(calls_used=1)
        second = store.read()['revision']
        store.update(data={'hold': True})
        third = store.read()['revision']
        self.assertGreater(second, first)
        self.assertGreater(third, second)

    def test_update_rejects_protected_fields(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        for field in ('revision', 'schema', 'config_digest', 'config',
                      'steps', 'current_step'):
            with self.assertRaises(ValueError):
                store.update(**{field: 'x'})
        store.update(phase='reconciliation_required', calls_used=3)
        state = store.read()
        self.assertEqual(state['phase'], 'reconciliation_required')
        self.assertEqual(state['calls_used'], 3)

    def test_update_publishes_projections(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.update(calls_used=2)
        projected = json.loads(
            (self.root / 'state.json').read_text(encoding='utf-8'))
        self.assertEqual(projected['revision'], store.read()['revision'])
        self.assertEqual(projected['calls_used'], 2)

    def test_begin_marks_step_running(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        store.begin('implement')
        state = store.read()
        self.assertEqual(state['current_step'], 'implement')
        self.assertEqual(state['phase'], 'running')
        self.assertEqual(state['steps'][0]['status'], 'running')
        self.assertEqual(state['steps'][1]['status'], 'pending')

    def test_begin_refuses_after_pause(self):
        from agent_coop.store import PausedError
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.pause()
        with self.assertRaises(PausedError):
            store.begin('implement')
        self.assertEqual(store.read()['steps'][0]['status'], 'pending')

    def test_finish_merges_updates_and_marks_done(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.begin('implement')
        store.finish('implement', {'delivered': True})
        state = store.read()
        self.assertEqual(state['steps'][0]['status'], 'done')
        self.assertIsNone(state['current_step'])
        self.assertEqual(state['data'], {'delivered': True})
        self.assertEqual(state['phase'], 'complete')

    def test_finish_preserves_concurrent_pause_hold_and_calls_used(self):
        writer = _make_store(self.root)
        writer.initialize({}, ['implement', 'verify'])
        cli = _make_store(self.root)
        writer.begin('implement')
        cli.update(data={'hold': True})
        cli.update(calls_used=3)
        cli.pause()
        writer.finish('implement', {'delivered': True})
        state = writer.read()
        self.assertEqual(state['steps'][0]['status'], 'done')
        self.assertEqual(state['data'], {'hold': True, 'delivered': True})
        self.assertEqual(state['calls_used'], 3)
        self.assertTrue(state['paused'])

    def test_fail_marks_blocked(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.begin('implement')
        store.fail('implement', 'boom')
        state = store.read()
        self.assertEqual(state['steps'][0]['status'], 'failed')
        self.assertEqual(state['phase'], 'blocked')
        self.assertEqual(state['error'], 'boom')
        self.assertIsNone(state['current_step'])

    def test_pause_resume_roundtrip(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.pause()
        self.assertTrue(store.read()['paused'])
        store.resume()
        self.assertFalse(store.read()['paused'])

    def test_resume_does_not_clear_failure(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.begin('implement')
        store.fail('implement', 'boom')
        with self.assertRaises(ValueError):
            store.resume()
        state = store.read()
        self.assertEqual(state['phase'], 'blocked')
        self.assertEqual(state['steps'][0]['status'], 'failed')
        self.assertFalse(state['paused'])
        self.assertIsNone(state['current_step'])
        self.assertEqual(state['error'], 'boom')

    def test_resume_refuses_residual_running(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.begin('implement')
        with self.assertRaises(ValueError):
            store.resume()
        state = store.read()
        self.assertEqual(state['phase'], 'running')
        self.assertEqual(state['steps'][0]['status'], 'running')
        self.assertFalse(state['paused'])

    def test_pause_conflict_propagates_and_persists(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        event0 = self.root / '.runtime' / 'outbox' / '000000.json'
        self.assertTrue(event0.exists(), event0)
        event0.write_text('{"revision": 0, "tampered": true}',
                          encoding='utf-8')
        with self.assertRaises(RuntimeError):
            store.pause()
        self.assertTrue(store.read()['paused'])

    def test_pause_lock_busy_defers_but_persists(self):
        from agent_coop.store import file_lock
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        with file_lock(store.publish_lock_path):
            store.pause()
        self.assertTrue(store.read()['paused'])
        store.publish()
        projected = json.loads(
            (self.root / 'state.json').read_text(encoding='utf-8'))
        self.assertTrue(projected['paused'])

    def test_publish_writes_two_projections_at_same_revision(self):
        store = _make_store(self.root)
        store.initialize({'policy': 'isolated-sample'}, ['implement'])
        store.update(data={'hold': False})
        store.publish()
        state_path = self.root / 'state.json'
        status_path = self.root / 'STATUS'
        self.assertTrue(state_path.exists(), state_path)
        self.assertTrue(status_path.exists(), status_path)
        projected = json.loads(state_path.read_text(encoding='utf-8'))
        self.assertEqual(projected['revision'], store.read()['revision'])
        self.assertEqual(projected['phase'], store.read()['phase'])
        self.assertIn(str(store.read()['revision']),
                      status_path.read_text(encoding='utf-8'))

    def test_publish_republish_does_not_regress_revision(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        store.publish()
        first = store.read()['revision']
        store.publish()
        self.assertEqual(store.read()['revision'], first)
        state_path = self.root / 'state.json'
        self.assertEqual(json.loads(state_path.read_text(encoding='utf-8'))['revision'],
                         first)
        store.update(data={'x': 1})
        second = store.read()['revision']
        self.assertGreater(second, first)
        store.publish()
        self.assertEqual(json.loads(state_path.read_text(encoding='utf-8'))['revision'],
                         second)


if __name__ == '__main__':
    unittest.main()
