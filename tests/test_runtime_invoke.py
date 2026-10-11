"""invoke 收据与显式子进程环境合同测试。

负例用 assertRaisesRegex 匹配真实原因关键词，不把 ImportError 当合格拒绝。
真实 Python 子进程验证 env 允许/剔除/四值覆盖与父环境不变，保留 env=None 入口。
sample.initialize 派生 profile→command/invoke 交接依赖包 A(sample) 的 schema2；
A 独立树未合入时相关用例失败属依赖待合，不冒称通过。
"""
import hashlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

from tests.test_runtime import (
    CODEBUDDY_SET,
    INHERIT,
    SubprocessTests,
    _sha256,
)


class InvokeTests(SubprocessTests):
    def test_success_returns_receipt(self):
        from agent_coop import adapters
        script = self._write_script(
            'import json\n'
            'print(json.dumps({"type":"system","subtype":"init",'
            '"session_id":"s1","model":"deepseek-v4-pro"}))\n'
            'print(json.dumps({"type":"result","is_error":False,'
            '"result":"{\\"ok\\":true}"}))\n'
        )
        profile = self._profile(script)
        with mock.patch.object(adapters, 'command',
                               return_value=[sys.executable, str(script)]):
            receipt = self._invoke(profile)
        self.assertEqual(receipt['exit_code'], 0)
        self.assertEqual(receipt['adapter'], 'codebuddy')
        self.assertEqual(receipt['actual_model'], 'deepseek-v4-pro')
        self.assertEqual(receipt['session_id'], 's1')
        self.assertEqual(receipt['requested_session_id'], 's1')
        self.assertEqual(receipt['result'], {'ok': True})
        self.assertGreaterEqual(receipt['wall_seconds'], 0)

    def test_verifies_executable_and_entry_hashes(self):
        from agent_coop import adapters
        marker = Path(self._tmp.name) / 'ran.txt'
        script = self._write_script(
            'import sys\nopen(sys.argv[1], "w").write("ran")\n'
        )
        argv = [sys.executable, str(script), str(marker)]
        for override in ({'entry_sha256': '0' * 64},
                         {'executable_sha256': '0' * 64}):
            with self.subTest(override=override):
                profile = self._profile(script, **override)
                with mock.patch.object(adapters, 'command', return_value=argv):
                    with self.assertRaisesRegex(Exception, '(?i)sha|hash'):
                        self._invoke(profile)
                self.assertFalse(marker.exists())

    def test_rejects_wrong_agent_file_hash(self):
        from agent_coop import adapters
        marker = Path(self._tmp.name) / 'ran.txt'
        script = self._write_script(
            'import sys\nopen(sys.argv[1], "w").write("ran")\n'
        )
        agent_file = self._write_script('# agent file\n', 'agent.md')
        profile = self._profile(script, adapter='kimi', agent_file=agent_file,
                                agent_file_sha256='0' * 64)
        argv = [sys.executable, str(script), str(marker)]
        with mock.patch.object(adapters, 'command', return_value=argv):
            with self.assertRaisesRegex(Exception, '(?i)sha|hash'):
                self._invoke(profile)
        self.assertFalse(marker.exists())

    def test_run_bounded_explicit_env_passes_to_child(self):
        script = self._write_script(
            'import json, os, sys\n'
            'keys = json.loads(sys.argv[1])\n'
            'print(json.dumps({k: os.environ.get(k) for k in keys}))\n'
        )
        keys = ['AGENT_COOP_INHERITED', 'AGENT_COOP_SECRET',
                'CODEBUDDY_DISABLE_AUTO_MEMORY', 'PATH']
        with mock.patch.dict(os.environ, {
                'AGENT_COOP_INHERITED': 'keep',
                'AGENT_COOP_SECRET': 'leak',
                'CODEBUDDY_DISABLE_AUTO_MEMORY': '0',
        }):
            env = {
                'PATH': os.environ.get('PATH', ''),
                'AGENT_COOP_INHERITED': 'keep',
                'CODEBUDDY_DISABLE_AUTO_MEMORY': '1',
            }
            result = self._run_bounded(
                [sys.executable, str(script), json.dumps(keys)], env=env)
        dumped = json.loads(result['stdout'])
        self.assertEqual(dumped['AGENT_COOP_INHERITED'], 'keep')
        self.assertIsNone(dumped['AGENT_COOP_SECRET'])
        self.assertEqual(dumped['CODEBUDDY_DISABLE_AUTO_MEMORY'], '1')
        self.assertIn('PATH', dumped)

    def test_explicit_env_does_not_modify_parent_environment(self):
        script = self._write_script('import sys\nsys.stdout.write("ok")\n')
        before = dict(os.environ)
        env = {'PATH': os.environ.get('PATH', '')}
        if os.name == 'nt':
            env['SYSTEMROOT'] = os.environ.get('SYSTEMROOT', '')
        self._run_bounded([sys.executable, str(script)], env=env)
        self.assertEqual(dict(os.environ), before)

    def test_env_none_inherits_parent_environment(self):
        with mock.patch.dict(os.environ, {'AGENT_COOP_PARENT_ONLY': 'present'}):
            script = self._write_script(
                'import os, sys\n'
                'sys.stdout.write(os.environ.get("AGENT_COOP_PARENT_ONLY", '
                '"missing"))\n'
            )
            result = self._run_bounded([sys.executable, str(script)])
        self.assertEqual(result['stdout'], 'present')

    def test_build_env_copies_inherit_applies_set_and_excludes_noninherit(self):
        from agent_coop.runtime import _build_env
        environment = {
            'inherit': ['PATH', 'SYSTEMROOT', 'AGENT_COOP_MISSING'],
            'set': {'CODEBUDDY_DISABLE_AUTO_MEMORY': '1'},
        }
        with mock.patch.dict(os.environ, {
                'CODEBUDDY_DISABLE_AUTO_MEMORY': '0',
                'AGENT_COOP_LEAK': 'secret',
        }):
            env = _build_env(environment)
        self.assertIn('PATH', env)
        if os.name == 'nt':
            self.assertIn('SYSTEMROOT', env)
        self.assertNotIn('AGENT_COOP_MISSING', env)
        self.assertNotIn('AGENT_COOP_LEAK', env)
        self.assertEqual(env['CODEBUDDY_DISABLE_AUTO_MEMORY'], '1')

    def test_build_env_applies_codebuddy_four_value_set(self):
        from agent_coop.runtime import _build_env
        environment = {'inherit': ['PATH', 'SYSTEMROOT'], 'set': CODEBUDDY_SET}
        with mock.patch.dict(os.environ, {
                'CODEBUDDY_DISABLE_AUTO_MEMORY': '0',
                'CODEBUDDY_CODE_DISABLE_AUTO_MEMORY': '0',
                'CODEBUDDY_MEMORY_EXTRACTION_ENABLED': '1',
                'CODEBUDDY_MEMORY_EXTRACTION_DISABLED': '0',
        }):
            env = _build_env(environment)
        self.assertEqual(env['CODEBUDDY_DISABLE_AUTO_MEMORY'], '1')
        self.assertEqual(env['CODEBUDDY_CODE_DISABLE_AUTO_MEMORY'], '1')
        self.assertEqual(env['CODEBUDDY_MEMORY_EXTRACTION_ENABLED'], '0')
        self.assertEqual(env['CODEBUDDY_MEMORY_EXTRACTION_DISABLED'], '1')

    def test_build_env_rejects_missing_path(self):
        from agent_coop.runtime import _build_env
        with self.assertRaisesRegex(ValueError, 'PATH'):
            _build_env({'inherit': [], 'set': {}})

    def test_build_env_rejects_missing_systemroot_on_windows(self):
        from agent_coop.runtime import _build_env
        if os.name != 'nt':
            self.skipTest('Windows-only SYSTEMROOT requirement')
        with self.assertRaisesRegex(ValueError, 'SYSTEMROOT'):
            _build_env({'inherit': ['PATH'], 'set': {}})

    def test_build_env_rejects_duplicate_or_case_ambiguous_inherit(self):
        from agent_coop.runtime import _build_env
        for names in (['PATH', 'PATH'], ['PATH', 'Path']):
            with self.subTest(names=names):
                with self.assertRaisesRegex(ValueError, 'inherit'):
                    _build_env({'inherit': names, 'set': {}})

    def test_build_env_rejects_non_string_set_values(self):
        from agent_coop.runtime import _build_env
        for value in (1, None, ['x']):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, 'set'):
                    _build_env({'inherit': [], 'set': {'K': value}})

    def test_build_env_rejects_case_ambiguous_set_keys(self):
        from agent_coop.runtime import _build_env
        cases = [
            ({'inherit': [], 'set': {'CODE': '1', 'code': '1'}}, 'set'),
            ({'inherit': ['PATH'], 'set': {'Path': 'x'}}, 'inherit'),
        ]
        for environment, pattern in cases:
            with self.subTest(environment=environment):
                with self.assertRaisesRegex(ValueError, pattern):
                    _build_env(environment)

    def test_build_env_allows_exact_same_name_set_override(self):
        from agent_coop.runtime import _build_env
        environment = {'inherit': ['PATH', 'SYSTEMROOT'],
                       'set': {'PATH': 'custom'}}
        env = _build_env(environment)
        self.assertEqual(env['PATH'], 'custom')

    def test_invoke_rejects_cwd_mismatch_before_launch(self):
        from agent_coop import adapters
        script = self._write_script(
            'import sys\nopen(sys.argv[1], "w").write("ran")\n')
        marker = Path(self._tmp.name) / 'ran.txt'
        profile = self._profile(script)
        profile['permissions']['root'] = (
            profile['permissions']['root'] + '/elsewhere')
        argv = [sys.executable, str(script), str(marker)]
        with mock.patch.object(adapters, 'command', return_value=argv) as cmd, \
                mock.patch('agent_coop.runtime.subprocess.Popen') as popen:
            with self.assertRaisesRegex(ValueError, 'cwd'):
                self._invoke(profile)
        cmd.assert_not_called()
        popen.assert_not_called()
        self.assertFalse(marker.exists())

    def test_sample_initialize_derives_profile_and_command(self):
        """依赖包 A(sample) schema2 权限派生；A 未合入时失败属依赖待合。"""
        from agent_coop import adapters, sample
        entry = self._write_script('# entry\n', 'entry.py')
        entry_hash = _sha256(entry)
        template = Path(sample.__file__).with_name('supervisor-agent.md')
        common = {
            'adapter': 'codebuddy', 'model': 'fixture',
            'executable': sys.executable,
            'executable_sha256': _sha256(sys.executable),
            'entry': str(entry), 'entry_sha256': entry_hash,
            'tools': ['Read', 'Glob', 'Grep'],
            'timeout_seconds': 600, 'output_limit_bytes': 8388608,
            'max_turns': 20,
        }
        profiles = {role: dict(common) for role in sample.ROLES}
        profiles['implement']['tools'] = common['tools'] + ['Write', 'Edit']
        profiles['supervise'].update(
            adapter='kimi', model=None, agent_file=str(template),
            agent_file_sha256=hashlib.sha256(template.read_bytes()).hexdigest())
        fresh = Path(self._tmp.name) / 'sample-init'
        state = sample.initialize(fresh, profiles)
        self.assertEqual(state['config']['schema'], 2)
        derived = state['config']['profiles']['implement']
        permissions = derived['permissions']
        self.assertEqual(permissions['schema'], 1)
        self.assertEqual(permissions['scope'], adapters.PERMISSION_SCOPE)
        self.assertEqual(permissions['root'], adapters.canonical_path(fresh))
        feature = adapters.canonical_path(fresh / 'workspace' / 'feature.py')
        self.assertEqual(permissions['write_files'], [feature])
        self.assertEqual(set(permissions['environment']), {'inherit', 'set'})
        argv = adapters.command(derived, 'hi', 's')
        self.assertIn(f'Write({feature})', argv)
        self.assertIn(f'Edit({feature})', argv)
        self.assertNotIn('acceptEdits', argv)

    def test_dispatch_reserves_budget_then_rejects_before_launch(self):
        """依赖包 A(sample) schema2；预留后启动前拒绝保留 +1 且无 Popen。"""
        from agent_coop import sample
        from agent_coop.store import Store
        entry = self._write_script('# entry\n', 'entry.py')
        entry_hash = _sha256(entry)
        template = Path(sample.__file__).with_name('supervisor-agent.md')
        common = {
            'adapter': 'codebuddy', 'model': 'fixture',
            'executable': sys.executable,
            'executable_sha256': _sha256(sys.executable),
            'entry': str(entry), 'entry_sha256': entry_hash,
            'tools': ['Read', 'Glob', 'Grep'],
            'timeout_seconds': 600, 'output_limit_bytes': 8388608,
            'max_turns': 20,
        }
        profiles = {role: dict(common) for role in sample.ROLES}
        profiles['implement']['tools'] = common['tools'] + ['Write', 'Edit']
        profiles['supervise'].update(
            adapter='kimi', model=None, agent_file=str(template),
            agent_file_sha256=hashlib.sha256(template.read_bytes()).hexdigest())
        fresh = Path(self._tmp.name) / 'sample-dispatch'
        state = sample.initialize(fresh, profiles)
        entry.write_text('# changed\n', encoding='utf-8')
        with mock.patch('agent_coop.runtime.subprocess.Popen') as popen:
            with self.assertRaisesRegex(ValueError, 'sha256'):
                sample.dispatch(fresh, state, 'implement', 'prompt')
        self.assertEqual(Store(fresh).read()['calls_used'], 1)
        popen.assert_not_called()


if __name__ == '__main__':
    unittest.main()
