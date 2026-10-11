"""Adapter 命令 argv 与权限字段校验的合同测试。

覆盖：结构化 argv、逗号分隔单 token 的 tools、逐条独立 allowedTools、
Write/Edit 精确文件规则、Bash/PowerShell 独立 disallowedTools、dontAsk 与
setting-sources none、禁止 acceptEdits/泛化、schema/scope/root 与工具写集
一致性、文件规则字符拒绝、Kimi 只读 agent-file。
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_coop import adapters
from tests.test_runtime import CODEBUDDY_SET, INHERIT


def _root():
    return adapters.canonical_path(os.path.join(os.getcwd(), 'fixture-root'))


def _feature():
    return adapters.canonical_path(
        os.path.join(os.getcwd(), 'fixture-root', 'workspace', 'feature.py'))


def _permissions(write_files):
    return {
        'schema': 1,
        'scope': adapters.PERMISSION_SCOPE,
        'root': _root(),
        'write_files': write_files,
        'environment': {'inherit': INHERIT, 'set': CODEBUDDY_SET},
    }


def _codebuddy_profile(**overrides):
    profile = {
        'adapter': 'codebuddy',
        'executable': 'C:/node/node.exe',
        'entry': 'C:/node/entry.js',
        'model': 'deepseek-v4-pro',
        'tools': ['Read', 'Glob', 'Grep', 'Write', 'Edit'],
        'max_turns': 20,
        'permissions': _permissions([_feature()]),
    }
    profile.update(overrides)
    return profile


def _kimi_profile(**overrides):
    profile = {
        'adapter': 'kimi',
        'executable': 'C:/kimi/kimi.exe',
        'entry': 'C:/kimi/entry.js',
        'agent_file': 'C:/kimi/agent.md',
        'model': None,
        'tools': ['Read', 'Glob', 'Grep'],
        'permissions': {
            'schema': 1,
            'scope': adapters.PERMISSION_SCOPE,
            'root': _root(),
            'write_files': [],
            'environment': {'inherit': INHERIT, 'set': {}},
        },
    }
    profile.update(overrides)
    return profile


def _values_after(argv, flag):
    return [argv[i + 1] for i, token in enumerate(argv)
            if token == flag and i + 1 < len(argv)]


class AdapterCommandTests(unittest.TestCase):
    def test_command_is_structured_argv_carrying_identity(self):
        profile = _codebuddy_profile()
        argv = adapters.command(profile, 'please implement', 'sess-1')
        self.assertIsInstance(argv, list)
        self.assertTrue(argv and all(isinstance(a, str) for a in argv))
        self.assertEqual(argv[0], profile['executable'])
        self.assertIn(profile['entry'], argv)
        self.assertIn('please implement', argv)
        self.assertIn('sess-1', argv)
        self.assertIn(profile['model'], argv)

    def test_command_requires_positive_max_turns(self):
        base = _codebuddy_profile()
        base.pop('max_turns')
        for bad in ({}, {'max_turns': 0}, {'max_turns': -1},
                    {'max_turns': '20'}, {'max_turns': True}):
            with self.subTest(max_turns=bad.get('max_turns', 'missing')):
                with self.assertRaisesRegex(ValueError, 'max_turns'):
                    adapters.command(dict(base, **bad), 'hi', 'sess-1')
        argv = adapters.command(dict(base, max_turns=20), 'hi', 'sess-1')
        self.assertIn('20', argv)

    def test_tools_are_comma_separated_single_token(self):
        argv = adapters.command(_codebuddy_profile(), 'hi', 's')
        self.assertEqual(_values_after(argv, '--tools'),
                         ['Read,Glob,Grep,Write,Edit'])

    def test_read_tools_are_independent_allowed_argv(self):
        profile = _codebuddy_profile(
            tools=['Read', 'Glob', 'Grep'], permissions=_permissions([]))
        argv = adapters.command(profile, 'hi', 's')
        self.assertEqual(_values_after(argv, '--allowedTools'),
                         ['Read', 'Glob', 'Grep'])

    def test_write_files_become_exact_write_and_edit_rules(self):
        argv = adapters.command(_codebuddy_profile(), 'hi', 's')
        allowed = _values_after(argv, '--allowedTools')
        self.assertIn(f'Write({_feature()})', allowed)
        self.assertIn(f'Edit({_feature()})', allowed)
        self.assertNotIn('Write', allowed)
        self.assertNotIn('Edit', allowed)

    def test_read_only_profile_emits_no_write_rules(self):
        profile = _codebuddy_profile(
            tools=['Read', 'Glob', 'Grep'], permissions=_permissions([]))
        argv = adapters.command(profile, 'hi', 's')
        allowed = _values_after(argv, '--allowedTools')
        self.assertFalse(any(v.startswith('Write(') or v.startswith('Edit(')
                             for v in allowed))

    def test_disallowed_tools_are_separate_bash_and_powershell(self):
        argv = adapters.command(_codebuddy_profile(), 'hi', 's')
        self.assertEqual(_values_after(argv, '--disallowedTools'),
                         ['Bash', 'PowerShell'])

    def test_permission_mode_dont_ask_without_accept_edits(self):
        argv = adapters.command(_codebuddy_profile(), 'hi', 's')
        self.assertEqual(_values_after(argv, '--permission-mode'), ['dontAsk'])
        self.assertEqual(_values_after(argv, '--setting-sources'), ['none'])
        self.assertNotIn('acceptEdits', argv)
        self.assertNotIn('bypassPermissions', argv)

    def test_pinned_identity_and_stream_json_preserved(self):
        argv = adapters.command(_codebuddy_profile(), 'hi', 'sess-9')
        self.assertEqual(_values_after(argv, '--model'), ['deepseek-v4-pro'])
        self.assertEqual(_values_after(argv, '--session-id'), ['sess-9'])
        self.assertEqual(_values_after(argv, '--max-turns'), ['20'])
        self.assertEqual(_values_after(argv, '--output-format'), ['stream-json'])
        self.assertEqual(_values_after(argv, '--mcp-config'),
                         ['{"mcpServers":{}}'])
        self.assertIn('--strict-mcp-config', argv)

    def test_write_tools_require_write_files(self):
        profile = _codebuddy_profile(permissions=_permissions([]))
        with self.assertRaisesRegex(ValueError, 'write_files'):
            adapters.command(profile, 'hi', 's')

    def test_read_only_tools_reject_write_files(self):
        profile = _codebuddy_profile(
            tools=['Read', 'Glob', 'Grep'],
            permissions=_permissions([_feature()]))
        with self.assertRaisesRegex(ValueError, 'write_files'):
            adapters.command(profile, 'hi', 's')

    def test_file_rule_rejects_forbidden_characters(self):
        for char in ('*', '?', '[', ']', '(', ')', '{', '}', ',', '!',
                     '\t', '\n'):
            with self.subTest(char=repr(char)):
                target = os.path.join(os.getcwd(), 'fixture-root', 'workspace',
                                      f'bad{char}name.py')
                profile = _codebuddy_profile(
                    permissions=_permissions([adapters.canonical_path(target)]))
                with self.assertRaisesRegex(ValueError, 'write rule'):
                    adapters.command(profile, 'hi', 's')

    def test_permissions_schema_must_be_integer_one(self):
        for bad in (True, False, 2, 0, '1', None, 1.0, 2.0):
            with self.subTest(schema=bad):
                profile = _codebuddy_profile()
                profile['permissions']['schema'] = bad
                with self.assertRaisesRegex(ValueError, 'schema'):
                    adapters.command(profile, 'hi', 's')

    def test_permissions_reject_unknown_key(self):
        profile = _codebuddy_profile()
        profile['permissions']['extra'] = 1
        with self.assertRaisesRegex(ValueError, 'permissions'):
            adapters.command(profile, 'hi', 's')

    def test_permissions_scope_must_match(self):
        profile = _codebuddy_profile()
        profile['permissions']['scope'] = 'other-scope'
        with self.assertRaisesRegex(ValueError, 'scope'):
            adapters.command(profile, 'hi', 's')

    def test_permissions_root_must_be_canonical(self):
        for bad in ('c:/TaskFixture/PilotRoot', 'C:\\TaskFixture\\PilotRoot',
                    'C:/TaskFixture/PilotRoot/', 'C:/TaskFixture/./PilotRoot',
                    'C:/TaskFixture/../PilotRoot'):
            with self.subTest(root=bad):
                profile = _codebuddy_profile()
                profile['permissions']['root'] = bad
                with self.assertRaisesRegex(ValueError, 'canonical'):
                    adapters.command(profile, 'hi', 's')

    def test_missing_permissions_rejected(self):
        profile = _codebuddy_profile()
        del profile['permissions']
        with self.assertRaisesRegex(ValueError, 'permissions'):
            adapters.command(profile, 'hi', 's')

    def test_environment_must_have_exactly_inherit_and_set(self):
        for env in ({}, {'inherit': INHERIT}, {'set': {}},
                    {'inherit': INHERIT, 'set': {}, 'extra': 1}):
            with self.subTest(environment=env):
                profile = _codebuddy_profile()
                profile['permissions']['environment'] = env
                with self.assertRaisesRegex(ValueError, 'inherit and set'):
                    adapters.command(profile, 'hi', 's')

    def test_kimi_keeps_agent_file_and_validates_read_only(self):
        argv = adapters.command(_kimi_profile(), 'please review', 'sess-1')
        self.assertEqual(argv[0], 'C:/kimi/kimi.exe')
        self.assertIn('--agent-file', argv)
        self.assertIn('C:/kimi/agent.md', argv)
        self.assertIn('please review', argv)
        self.assertIn('--output-format', argv)
        self.assertIn('stream-json', argv)

    def test_kimi_rejects_write_files(self):
        profile = _kimi_profile()
        profile['permissions']['write_files'] = [_feature()]
        with self.assertRaisesRegex(ValueError, 'write_files'):
            adapters.command(profile, 'hi', 's')

    def test_kimi_rejects_write_files_even_with_write_tools(self):
        profile = _kimi_profile(tools=['Read', 'Glob', 'Grep', 'Write', 'Edit'])
        profile['permissions']['write_files'] = [_feature()]
        with self.assertRaisesRegex(ValueError, 'write_files'):
            adapters.command(profile, 'hi', 's')

    def test_canonical_path_matches_sample_representation(self):
        from agent_coop import sample
        for path in (os.getcwd(), _root(), _feature()):
            with self.subTest(path=path):
                self.assertEqual(adapters.canonical_path(path),
                                 sample.canonical_path(path))

    def test_canonical_path_rejects_reparse_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            outside = base / 'outside'
            outside.mkdir()
            link = base / 'link'
            if sys.platform == 'win32':
                proc = subprocess.run(
                    ['cmd', '/c', 'mklink', '/J', str(link), str(outside)],
                    capture_output=True, text=True)
                if proc.returncode != 0:
                    self.skipTest(f'mklink /J unavailable: {proc.stderr.strip()}')
            else:
                try:
                    link.symlink_to(outside, target_is_directory=True)
                except OSError as exc:
                    self.skipTest(f'symlink unavailable: {exc}')
            with self.assertRaisesRegex(ValueError, 'symlink or junction'):
                adapters.canonical_path(link / 'inner' / 'file.py')


if __name__ == '__main__':
    unittest.main()
