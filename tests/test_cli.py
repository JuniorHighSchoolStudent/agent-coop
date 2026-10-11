"""CLI 真实进程入口与本地只读状态面。"""
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_help_exposes_explicit_lifecycle_commands(self):
        result = subprocess.run(
            [sys.executable, '-m', 'agent_coop', '--help'],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ('init', 'run', 'status', 'pause', 'resume', 'serve', 'verify'):
            self.assertIn(command, result.stdout)

    def test_init_refuses_incomplete_profiles_without_creating_root(self):
        with tempfile.TemporaryDirectory() as directory:
            profiles = Path(directory) / 'profiles.json'
            profiles.write_text('{}', encoding='utf-8')
            root = Path(directory) / 'sample'
            result = subprocess.run(
                [sys.executable, '-m', 'agent_coop', 'init', str(root),
                 '--profiles', str(profiles)],
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(root.exists())
            self.assertIn('profiles', result.stderr)

    def test_init_rejects_supplied_permissions_before_root_creation(self):
        from agent_coop.sample import ROLES
        with tempfile.TemporaryDirectory() as directory:
            profiles = Path(directory) / 'profiles.json'
            injected = {role: {'permissions': {'schema': 1}} for role in ROLES}
            profiles.write_text(json.dumps(injected), encoding='utf-8')
            root = Path(directory) / 'sample'
            result = subprocess.run(
                [sys.executable, '-m', 'agent_coop', 'init', str(root),
                 '--profiles', str(profiles)],
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(root.exists())
            self.assertIn('permissions', result.stderr)

    def test_self_reported_readonly_profile_cannot_load_shell_agent(self):
        from agent_coop.sample import ROLES, validate_profiles
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / 'runtime.js'
            runtime.write_text('// unused offline fixture', encoding='utf-8')
            value = hashlib.sha256(runtime.read_bytes()).hexdigest()
            common = {'adapter': 'codebuddy', 'model': 'test', 'executable': str(runtime),
                      'entry': str(runtime), 'executable_sha256': value, 'entry_sha256': value,
                      'timeout_seconds': 600, 'output_limit_bytes': 8388608, 'max_turns': 20,
                      'tools': ['Read', 'Glob', 'Grep']}
            profiles = {role: dict(common) for role in ROLES}
            profiles['implement']['tools'] = common['tools'] + ['Write', 'Edit']
            dangerous = Path(directory) / 'supervisor.md'
            dangerous.write_text('---\ntools: [Read, Shell]\n---\n', encoding='utf-8')
            profiles['supervise'].update(
                adapter='kimi', model=None, agent_file=str(dangerous),
                agent_file_sha256=hashlib.sha256(dangerous.read_bytes()).hexdigest(),
            )
            with self.assertRaisesRegex(ValueError, 'read-only template'):
                validate_profiles(profiles)

    def _cli(self, *args):
        return subprocess.run(
            [sys.executable, '-m', 'agent_coop', *args],
            capture_output=True, text=True, timeout=10,
        )

    def test_status_pause_resume_persist_same_store(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            Store(root).initialize({'mode': 'test'}, ['one'])
            status = self._cli('status', str(root))
            self.assertEqual(status.returncode, 0, status.stderr)
            first = json.loads(status.stdout)
            self.assertEqual(first['phase'], 'ready')
            paused = self._cli('pause', str(root))
            self.assertEqual(paused.returncode, 0, paused.stderr)
            after_pause = json.loads(paused.stdout)
            self.assertTrue(after_pause['paused'])
            self.assertGreater(after_pause['revision'], first['revision'])
            resumed = self._cli('resume', str(root))
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            after_resume = json.loads(resumed.stdout)
            self.assertFalse(after_resume['paused'])
            self.assertGreater(after_resume['revision'], after_pause['revision'])
            final_run = self._cli('status', str(root))
            self.assertEqual(final_run.returncode, 0, final_run.stderr)
            final = json.loads(final_run.stdout)
            self.assertEqual(final['revision'], after_resume['revision'])
            self.assertFalse(final['paused'])

    def test_blocked_and_reconciliation_are_nonzero_and_not_cleared(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            store = Store(root)
            store.initialize({'mode': 'test'}, ['one'])
            store.update(phase='blocked')
            blocked = self._cli('status', str(root))
            self.assertEqual(blocked.returncode, 1, blocked.stderr)
            refused = self._cli('resume', str(root))
            self.assertEqual(refused.returncode, 1, refused.stderr)
            self.assertNotIn('Traceback', refused.stderr)
            self.assertTrue(refused.stderr.strip())
            self.assertEqual(Store(root).read()['phase'], 'blocked')
            store.update(phase='reconciliation_required')
            recon = self._cli('status', str(root))
            self.assertEqual(recon.returncode, 1, recon.stderr)
            refused = self._cli('resume', str(root))
            self.assertEqual(refused.returncode, 1, refused.stderr)
            self.assertNotIn('Traceback', refused.stderr)
            self.assertTrue(refused.stderr.strip())
            self.assertEqual(Store(root).read()['phase'], 'reconciliation_required')

    def test_run_rejects_negative_max_steps_without_side_effects(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            store = Store(root)
            store.initialize({'mode': 'test'}, ['one'])
            before = store.read()['revision']
            result = self._cli('run', str(root), '--max-steps=-1')
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn('max-steps', result.stderr)
            self.assertEqual(Store(root).read()['revision'], before)
            self.assertFalse((root / '.runtime' / 'run.lock').exists())

    def test_run_accepts_zero_max_steps(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            Store(root).initialize({'mode': 'test'}, ['one'])
            result = self._cli('run', str(root), '--max-steps', '0')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_serve_rejects_out_of_range_port(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            Store(root).initialize({'mode': 'test'}, ['one'])
            result = self._cli('serve', str(root), '--port', '70000')
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn('port', result.stderr)

    def test_corrupt_store_yields_clean_nonzero_result(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            store = Store(root)
            store.initialize({'mode': 'test'}, ['one'])
            (root / '.runtime' / 'state.sqlite').write_bytes(b'not a sqlite database')
            result = self._cli('status', str(root))
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertTrue(result.stderr.strip())


if __name__ == '__main__':
    unittest.main()
