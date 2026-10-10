"""Runtime 子进程边界与 adapter 身份/协议解析的合同测试。

负例用 assertRaisesRegex 匹配真实原因关键词，不把 ImportError 当合格拒绝；
run_bounded 驱动真实临时 Python 子进程验证成功/非零退出/输出上限/超时进程树、
孤儿继承管道、日志隔离与有界落盘、SHA 重验与 ResourceWarning 回收。
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def remove_link(path):
    """仅移除 junction/符号链接自身，不递归其目标。"""
    path = Path(path)
    for cleaner in (os.rmdir, os.unlink):
        try:
            cleaner(path)
            return
        except OSError:
            continue


def _parse(profile, stdout, session_id):
    from agent_coop import adapters
    return adapters.parse(profile, stdout, session_id)


CODEBUDDY = {'adapter': 'codebuddy', 'model': 'deepseek-v4-pro',
             'tools': ['Read', 'Glob', 'Grep', 'Write', 'Edit']}
KIMI = {'adapter': 'kimi', 'model': None,
        'tools': ['Read', 'Glob', 'Grep']}


class AdapterParseTests(unittest.TestCase):
    def test_codebuddy_uses_result_event_not_trailing_hook(self):
        stdout = (
            '{"type":"system","subtype":"init","session_id":"s1",'
            '"model":"deepseek-v4-pro"}\n'
            '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n'
            '{"type":"hook","event":"Stop","result":"{\\"bad\\":true}"}\n'
        )
        self.assertEqual(_parse(CODEBUDDY, stdout, 's1')['result'],
                         {'ok': True})

    def test_codebuddy_requires_matching_init_model_and_session(self):
        ok = ('{"type":"system","subtype":"init","session_id":"s1",'
              '"model":"deepseek-v4-pro"}\n'
              '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n')
        bad_model = ok.replace('deepseek-v4-pro', 'glm-5.3', 1)
        bad_session = ('{"type":"system","subtype":"init","session_id":"other",'
                       '"model":"deepseek-v4-pro"}\n'
                       '{"type":"result","is_error":false,'
                       '"result":"{\\"ok\\":true}"}\n')
        self.assertEqual(_parse(CODEBUDDY, ok, 's1')['result'], {'ok': True})
        with self.assertRaisesRegex(ValueError, 'model'):
            _parse(CODEBUDDY, bad_model, 's1')
        with self.assertRaisesRegex(ValueError, 'session'):
            _parse(CODEBUDDY, bad_session, 's1')

    def test_codebuddy_rejects_error_and_non_json_result(self):
        error = ('{"type":"system","subtype":"init","session_id":"s1",'
                 '"model":"deepseek-v4-pro"}\n'
                 '{"type":"result","is_error":true,"result":"boom"}\n')
        non_json = ('{"type":"system","subtype":"init","session_id":"s1",'
                    '"model":"deepseek-v4-pro"}\n'
                    '{"type":"result","is_error":false,"result":"not json"}\n')
        with self.assertRaisesRegex(ValueError, 'error'):
            _parse(CODEBUDDY, error, 's1')
        with self.assertRaisesRegex(ValueError, 'json'):
            _parse(CODEBUDDY, non_json, 's1')

    def test_codebuddy_reports_requested_and_actual_identity(self):
        stdout = ('{"type":"system","subtype":"init","session_id":"s1",'
                  '"model":"deepseek-v4-pro"}\n'
                  '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n')
        receipt = _parse(CODEBUDDY, stdout, 's1')
        self.assertEqual(receipt['adapter'], 'codebuddy')
        self.assertEqual(receipt['requested_model'], 'deepseek-v4-pro')
        self.assertEqual(receipt['actual_model'], 'deepseek-v4-pro')
        self.assertEqual(receipt['requested_session_id'], 's1')
        self.assertEqual(receipt['session_id'], 's1')

    def test_codebuddy_raw_text_is_final_result_only(self):
        stdout = (
            '{"type":"system","subtype":"init","session_id":"s1",'
            '"model":"deepseek-v4-pro"}\n'
            '{"type":"assistant","message":{"content":['
            '{"type":"tool_use","name":"Read"}]}}\n'
            '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n'
        )
        receipt = _parse(CODEBUDDY, stdout, 's1')
        self.assertEqual(receipt['raw_text'], '{"ok":true}')
        self.assertNotIn('tool_use', receipt['raw_text'])
        self.assertNotIn('init', receipt['raw_text'])

    def test_codebuddy_allowed_tool_error_is_counted_not_fatal(self):
        stdout = (
            '{"type":"system","subtype":"init","session_id":"s1",'
            '"model":"deepseek-v4-pro"}\n'
            '{"type":"user","message":{"content":['
            '{"type":"tool_result","is_error":true}]}}\n'
            '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n'
        )
        receipt = _parse(CODEBUDDY, stdout, 's1')
        self.assertEqual(receipt['result'], {'ok': True})
        self.assertEqual(receipt['tool_errors'], 1)

    def test_codebuddy_tool_outside_profile_is_blocked(self):
        stdout = (
            '{"type":"system","subtype":"init","session_id":"s1",'
            '"model":"deepseek-v4-pro"}\n'
            '{"type":"assistant","message":{"content":['
            '{"type":"tool_use","name":"Bash"}]}}\n'
            '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n'
        )
        with self.assertRaisesRegex(ValueError, 'tool'):
            _parse(CODEBUDDY, stdout, 's1')

    def test_parse_rejects_bad_jsonl_line(self):
        stdout = (
            '{"type":"system","subtype":"init","session_id":"s1",'
            '"model":"deepseek-v4-pro"}\n'
            'this is not json\n'
            '{"type":"result","is_error":false,"result":"{\\"ok\\":true}"}\n'
        )
        with self.assertRaisesRegex(ValueError, 'JSONL'):
            _parse(CODEBUDDY, stdout, 's1')

    def test_parse_rejects_dict_result(self):
        stdout = (
            '{"type":"system","subtype":"init","session_id":"s1",'
            '"model":"deepseek-v4-pro"}\n'
            '{"type":"result","is_error":false,"result":{"ok":true}}\n'
        )
        with self.assertRaisesRegex(ValueError, 'json'):
            _parse(CODEBUDDY, stdout, 's1')

    def test_kimi_uses_final_assistant_content_and_resume_hint(self):
        stdout = (
            '{"role":"meta","type":"system.version","version":"0.43.0"}\n'
            '{"role":"assistant","content":"{\\"ok\\":true}"}\n'
            '{"role":"meta","type":"session.resume_hint",'
            '"session_id":"session_native1"}\n'
        )
        receipt = _parse(KIMI, stdout, 'req-123')
        self.assertEqual(receipt['result'], {'ok': True})
        self.assertIsNone(receipt['actual_model'])
        self.assertEqual(receipt['session_id'], 'session_native1')
        self.assertEqual(receipt['requested_session_id'], 'req-123')

    def test_kimi_blocks_without_resume_hint(self):
        stdout = (
            '{"role":"meta","type":"system.version","version":"0.43.0"}\n'
            '{"role":"assistant","content":"{\\"ok\\":true}"}\n'
        )
        with self.assertRaisesRegex(ValueError, 'resume_hint'):
            _parse(KIMI, stdout, 'req-123')

    def test_kimi_rejects_tool_calls_and_non_json_content(self):
        tool_calls = ('{"role":"assistant","tool_calls":[{"id":"1"}]}\n'
                      '{"role":"meta","type":"session.resume_hint",'
                      '"session_id":"session_native1"}\n')
        plain_text = ('{"role":"assistant","content":"just some words"}\n'
                      '{"role":"meta","type":"session.resume_hint",'
                      '"session_id":"session_native1"}\n')
        with self.assertRaisesRegex(ValueError, 'tool'):
            _parse(KIMI, tool_calls, 'req-123')
        with self.assertRaisesRegex(ValueError, 'json'):
            _parse(KIMI, plain_text, 'req-123')


class AdapterCommandTests(unittest.TestCase):
    def test_command_is_structured_argv_carrying_identity(self):
        from agent_coop import adapters
        profile = {'adapter': 'codebuddy', 'executable': '/node',
                   'entry': '/entry.js', 'model': 'deepseek-v4-pro',
                   'tools': [], 'max_turns': 20}
        argv = adapters.command(profile, 'please implement', 'sess-1')
        self.assertIsInstance(argv, list)
        self.assertTrue(argv and all(isinstance(a, str) for a in argv))
        self.assertEqual(argv[0], profile['executable'])
        self.assertIn(profile['entry'], argv)
        self.assertIn('please implement', argv)
        self.assertIn('sess-1', argv)
        self.assertIn(profile['model'], argv)

    def test_command_requires_positive_max_turns(self):
        from agent_coop import adapters
        base = {'adapter': 'codebuddy', 'executable': '/node',
                'entry': '/entry.js', 'model': 'deepseek-v4-pro', 'tools': []}
        for bad in ({}, {'max_turns': 0}, {'max_turns': -1},
                    {'max_turns': '20'}):
            with self.subTest(max_turns=bad.get('max_turns', 'missing')):
                with self.assertRaisesRegex(ValueError, 'max_turns'):
                    adapters.command(dict(base, **bad), 'hi', 'sess-1')
        argv = adapters.command(dict(base, max_turns=20), 'hi', 'sess-1')
        self.assertIn('20', argv)


class SubprocessTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        base = Path(self._tmp.name)
        self.root = base / 'sample'
        self.root.mkdir()
        (self.root / '.agent-coop-sample').write_text('sample', encoding='utf-8')
        self.log_dir = self.root / '.runtime' / 'logs'
        self.log_dir.mkdir(parents=True)

    def _write_script(self, body, name='fixture.py'):
        script = Path(self._tmp.name) / name
        script.write_text(body, encoding='utf-8')
        return script

    def _run_bounded(self, argv, **overrides):
        from agent_coop.runtime import run_bounded
        kwargs = dict(argv=argv, cwd=str(self.root), log_dir=str(self.log_dir),
                      timeout_seconds=30, output_limit_bytes=1_000_000)
        kwargs.update(overrides)
        return run_bounded(**kwargs)

    def _profile(self, script, adapter='codebuddy', agent_file=None, **overrides):
        profile = {
            'adapter': adapter,
            'executable': sys.executable,
            'entry': str(script),
            'executable_sha256': _sha256(sys.executable),
            'entry_sha256': _sha256(script),
            'model': 'deepseek-v4-pro' if adapter == 'codebuddy' else None,
            'tools': ['Read'],
            'timeout_seconds': 30,
            'output_limit_bytes': 1_000_000,
            'max_turns': 20,
            'agent_file': str(agent_file) if agent_file else None,
            'agent_file_sha256': _sha256(agent_file) if agent_file else None,
        }
        profile.update(overrides)
        return profile

    def _invoke(self, profile, prompt='hi', session_id='s1'):
        from agent_coop.runtime import invoke
        return invoke(profile, prompt, str(self.root), str(self.log_dir),
                      session_id)


class RunBoundedTests(SubprocessTests):
    def test_success_returns_text_hashes_and_timing(self):
        script = self._write_script(
            'import sys\n'
            'sys.stdout.write("hello world")\n'
            'sys.stderr.write("warn")\n'
        )
        result = self._run_bounded([sys.executable, str(script)])
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(result['stdout'], 'hello world')
        self.assertEqual(result['stderr'], 'warn')
        self.assertEqual(result['stdout_sha256'], _sha256_text('hello world'))
        self.assertEqual(result['stderr_sha256'], _sha256_text('warn'))
        self.assertGreaterEqual(result['wall_seconds'], 0)

    def test_nonzero_exit_raises(self):
        script = self._write_script('import sys\nsys.exit(3)\n')
        with self.assertRaisesRegex(Exception, '(?i)exit'):
            self._run_bounded([sys.executable, str(script)])

    def test_output_limit_raises(self):
        script = self._write_script(
            'import sys\n'
            'sys.stdout.write("A" * 200)\n'
            'sys.stderr.write("B" * 200)\n'
        )
        with self.assertRaisesRegex(Exception, '(?i)exceed'):
            self._run_bounded([sys.executable, str(script)],
                              output_limit_bytes=300)

    def test_timeout_terminates_process_tree(self):
        parent = self._write_script(
            'import subprocess, sys, time\n'
            'subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2],'
            ' sys.argv[3]])\n'
            'time.sleep(30)\n',
            'parent.py',
        )
        child = self._write_script(
            'import sys, time\n'
            'open(sys.argv[1], "w").write("ready")\n'
            'time.sleep(10)\n'
            'open(sys.argv[2], "w").write("survived")\n',
            'child.py',
        )
        ready = Path(self._tmp.name) / 'ready.txt'
        survived = Path(self._tmp.name) / 'survived.txt'
        argv = [sys.executable, str(parent), str(child), str(ready),
                str(survived)]
        with self.assertRaisesRegex(Exception, '(?i)timeout'):
            self._run_bounded(argv, timeout_seconds=2)
        self.assertTrue(ready.exists())
        time.sleep(11)
        self.assertFalse(survived.exists())

    def test_log_dir_outside_root_is_rejected(self):
        script = self._write_script('import sys\nsys.stdout.write("x")\n')
        outside = Path(self._tmp.name) / 'outside'
        outside.mkdir()
        with self.assertRaisesRegex(Exception, 'log_dir'):
            self._run_bounded([sys.executable, str(script)],
                              log_dir=str(outside))

    def test_log_dir_inside_root_but_outside_runtime_is_rejected(self):
        script = self._write_script('import sys\nsys.stdout.write("x")\n')
        with self.assertRaisesRegex(ValueError, 'log_dir'):
            self._run_bounded([sys.executable, str(script)],
                              log_dir=str(self.root / 'workspace'))

    def test_log_dir_junction_escape_is_rejected(self):
        outside = Path(self._tmp.name) / 'outside'
        outside.mkdir()
        sentinel = outside / 'sentinel.txt'
        sentinel.write_text('untouched', encoding='utf-8')
        marker = Path(self._tmp.name) / 'child_ran.txt'
        script = self._write_script(
            'import sys\n'
            'open(sys.argv[1], "w").write("ran")\n',
            'escape_child.py',
        )
        junction = self.root / '.runtime' / 'escape'
        if sys.platform == 'win32':
            proc = subprocess.run(
                ['cmd', '/c', 'mklink', '/J', str(junction), str(outside)],
                capture_output=True, text=True)
            if proc.returncode != 0:
                self.skipTest(f'mklink /J 不可用: {proc.stderr.strip()}')
        else:
            try:
                junction.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f'symlink 不可用: {exc}')
        self.addCleanup(remove_link, junction)
        with self.assertRaisesRegex(ValueError, 'junction|symlink'):
            self._run_bounded([sys.executable, str(script), str(marker)],
                              log_dir=str(junction))
        self.assertFalse(marker.exists())
        self.assertEqual(sentinel.read_text(encoding='utf-8'), 'untouched')
        self.assertEqual([p.name for p in outside.iterdir()], ['sentinel.txt'])

    def test_log_dir_accepts_runtime_and_its_descendants(self):
        script = self._write_script('import sys\nsys.stdout.write("ok")\n')
        for rel in ('.runtime', '.runtime/verification'):
            with self.subTest(log_dir=rel):
                result = self._run_bounded(
                    [sys.executable, str(script)],
                    log_dir=str(self.root / rel))
                self.assertEqual(result['stdout'], 'ok')

    def test_log_bytes_are_bounded_on_disk(self):
        script = self._write_script(
            'import sys\n'
            'sys.stdout.write("A" * 200)\n'
            'sys.stderr.write("B" * 200)\n'
        )
        with self.assertRaisesRegex(Exception, '(?i)exceed'):
            self._run_bounded([sys.executable, str(script)],
                              output_limit_bytes=300)
        stdout_log = self.log_dir / 'stdout.log'
        stderr_log = self.log_dir / 'stderr.log'
        self.assertTrue(stdout_log.exists())
        self.assertTrue(stderr_log.exists())
        total = stdout_log.stat().st_size + stderr_log.stat().st_size
        self.assertLessEqual(total, 300)

    def test_parent_exit_with_child_holding_pipe_is_bounded_failure(self):
        parent = self._write_script(
            'import subprocess, sys\n'
            'subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2]])\n',
            'parent.py',
        )
        child = self._write_script(
            'import sys, time\n'
            'open(sys.argv[1], "w").write("ready")\n'
            'time.sleep(3)\n',
            'child.py',
        )
        ready = Path(self._tmp.name) / 'orphan_ready.txt'
        with self.assertRaisesRegex(Exception, '(?i)timeout'):
            self._run_bounded(
                [sys.executable, str(parent), str(child), str(ready)],
                timeout_seconds=1)
        self.assertTrue(ready.exists())
        time.sleep(3)

    def test_success_leaves_no_resource_warning(self):
        import gc
        import warnings
        script = self._write_script('import sys\nsys.stdout.write("ok")\n')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            self._run_bounded([sys.executable, str(script)])
            gc.collect()
        self.assertFalse(
            any(issubclass(w.category, ResourceWarning) for w in caught))


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


if __name__ == '__main__':
    unittest.main()
