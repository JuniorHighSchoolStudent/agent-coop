"""Runner 唯一有界驱动：顺序、跳过、暂停、失败与互斥的合同测试。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _make_store(root):
    from agent_coop.store import Store
    return Store(root)


def _make_runner(root, handlers):
    from agent_coop.runner import Runner
    return Runner(root, handlers)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / 'sample'
        (self.root / '.runtime').mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_runs_steps_in_order_and_completes(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify', 'review'])
        calls = []

        def handler_for(name):
            def handler(state):
                calls.append(name)
                return {name: True}
            return handler

        handlers = {n: handler_for(n)
                    for n in ('implement', 'verify', 'review')}
        _make_runner(self.root, handlers).run()
        self.assertEqual(calls, ['implement', 'verify', 'review'])
        state = store.read()
        self.assertEqual(state['phase'], 'complete')
        self.assertEqual([s['status'] for s in state['steps']],
                         ['done', 'done', 'done'])
        self.assertEqual(state['data'],
                         {'implement': True, 'verify': True, 'review': True})

    def test_already_done_steps_are_not_rerun(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        calls = []

        def implement(state):
            calls.append('implement')
            return {}

        runner = _make_runner(self.root, {'implement': implement})
        runner.run()
        runner.run()
        self.assertEqual(calls, ['implement'])
        self.assertEqual(store.read()['phase'], 'complete')

    def test_max_steps_bounds_dispatch(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify', 'review'])
        calls = []

        def handler_for(name):
            def handler(state):
                calls.append(name)
                return {}
            return handler

        handlers = {n: handler_for(n)
                    for n in ('implement', 'verify', 'review')}
        _make_runner(self.root, handlers).run(max_steps=2)
        self.assertEqual(calls, ['implement', 'verify'])
        state = store.read()
        self.assertEqual(state['steps'][2]['status'], 'pending')
        self.assertNotEqual(state['phase'], 'complete')

    def test_max_steps_rejects_bool_and_negative(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        handlers = {'implement': lambda s: {}}
        with self.assertRaises(ValueError):
            _make_runner(self.root, handlers).run(max_steps=True)
        with self.assertRaises(ValueError):
            _make_runner(self.root, handlers).run(max_steps=-1)

    def test_pause_persists_and_stops_after_current_step(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        calls = []

        def implement(state):
            calls.append('implement')
            _make_store(self.root).pause()
            return {'done_impl': True}

        def verify(state):
            calls.append('verify')
            return {'done_verify': True}

        _make_runner(self.root, {'implement': implement, 'verify': verify}).run()
        self.assertEqual(calls, ['implement'])
        state = store.read()
        self.assertTrue(state['paused'])
        self.assertEqual(state['steps'][0]['status'], 'done')
        self.assertEqual(state['steps'][1]['status'], 'pending')
        store.resume()
        _make_runner(self.root, {'implement': implement, 'verify': verify}).run()
        self.assertEqual(calls, ['implement', 'verify'])
        self.assertEqual(store.read()['phase'], 'complete')

    def test_handler_failure_blocks_without_auto_retry(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        calls = []

        def implement(state):
            calls.append('implement')
            return {}

        def verify(state):
            calls.append('verify')
            raise RuntimeError('boom')

        runner = _make_runner(self.root, {'implement': implement, 'verify': verify})
        runner.run()
        state = store.read()
        self.assertEqual(calls, ['implement', 'verify'])
        self.assertEqual(state['steps'][0]['status'], 'done')
        self.assertEqual(state['steps'][1]['status'], 'failed')
        self.assertEqual(state['phase'], 'blocked')
        self.assertIn('boom', state['error'])
        runner.run()
        self.assertEqual(calls, ['implement', 'verify'])

    def test_handler_non_dict_result_blocks(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement'])
        calls = []

        def implement(state):
            calls.append('implement')
            return 'not-a-dict'

        _make_runner(self.root, {'implement': implement}).run()
        state = store.read()
        self.assertEqual(state['steps'][0]['status'], 'failed')
        self.assertEqual(state['phase'], 'blocked')
        self.assertIn('non-dict', state['error'])
        _make_runner(self.root, {'implement': implement}).run()
        self.assertEqual(calls, ['implement'])

    def test_residual_running_requires_reconciliation(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        store.begin('implement')
        calls = []

        def implement(state):
            calls.append('implement')
            return {}

        _make_runner(self.root, {'implement': implement,
                                 'verify': lambda s: {}}).run()
        self.assertEqual(calls, [])
        state = store.read()
        self.assertEqual(state['phase'], 'reconciliation_required')
        self.assertEqual(state['steps'][0]['status'], 'running')

    def test_second_runner_is_refused_while_first_runs(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        outcome = {}

        def implement(state):
            nested = _make_runner(self.root, {'verify': lambda s: {}})
            try:
                nested.run()
                outcome['nested'] = 'ran'
            except Exception as exc:
                outcome['nested'] = type(exc).__name__
            return {}

        _make_runner(self.root, {'implement': implement,
                                 'verify': lambda s: {}}).run()
        self.assertNotEqual(outcome.get('nested'), 'ran')
        self.assertEqual(store.read()['phase'], 'complete')

    def test_handler_budget_updates_survive_finish(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])

        def bump(state):
            s = _make_store(self.root)
            s.update(calls_used=s.read()['calls_used'] + 1)
            return {}

        _make_runner(self.root, {'implement': bump, 'verify': bump}).run()
        self.assertEqual(store.read()['calls_used'], 2)

    def test_run_publishes_projections(self):
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        _make_runner(self.root, {
            'implement': lambda s: {'a': 1},
            'verify': lambda s: {},
        }).run()
        state = store.read()
        projected = json.loads(
            (self.root / 'state.json').read_text(encoding='utf-8'))
        self.assertEqual(projected['revision'], state['revision'])
        self.assertEqual(projected['phase'], 'complete')
        self.assertEqual([s['status'] for s in projected['steps']],
                         ['done', 'done'])
        self.assertTrue((self.root / 'STATUS').exists())

    def test_publish_failure_keeps_done_and_no_redispatch(self):
        from agent_coop import store as store_mod
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        original = store_mod.Store.publish
        fail = {'on': False}

        def flaky(self):
            if fail['on']:
                raise OSError('disk full')
            return original(self)

        store_mod.Store.publish = flaky
        try:
            calls = []

            def implement(state):
                calls.append('implement')
                fail['on'] = True
                return {'impl': True}

            def verify(state):
                calls.append('verify')
                return {}

            runner = _make_runner(self.root, {
                'implement': implement, 'verify': verify})
            with self.assertRaises(OSError):
                runner.run()
        finally:
            store_mod.Store.publish = original

        state = store.read()
        self.assertEqual(state['steps'][0]['status'], 'done')
        self.assertEqual(state['steps'][1]['status'], 'pending')
        self.assertEqual(state['data'], {'impl': True})

        calls2 = []

        def verify2(state):
            calls2.append('verify')
            return {}

        _make_runner(self.root, {'verify': verify2}).run()
        self.assertEqual(calls, ['implement'])
        self.assertEqual(calls2, ['verify'])
        self.assertEqual(store.read()['phase'], 'complete')

    def test_cross_process_runner_mutex(self):
        from agent_coop.store import file_lock
        store = _make_store(self.root)
        store.initialize({}, ['implement', 'verify'])
        project_root = Path(__file__).resolve().parent.parent
        lock_path = self.root / '.runtime' / 'run.lock'
        code = (
            'import sys\n'
            'from agent_coop.runner import Runner\n'
            'Runner(sys.argv[1], {"implement": lambda s: {}, '
            '"verify": lambda s: {}}).run()\n'
            'print("RAN")\n'
        )
        env = dict(os.environ)
        env['PYTHONPATH'] = (str(project_root) + os.pathsep
                             + env.get('PYTHONPATH', ''))
        with file_lock(lock_path):
            proc = subprocess.run(
                [sys.executable, '-c', code, str(self.root)],
                capture_output=True, text=True, env=env, timeout=60,
            )
        self.assertNotIn('RAN', proc.stdout, proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
