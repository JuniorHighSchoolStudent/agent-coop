"""门禁不采信 PASS 文字或旧候选。"""
import json
import tempfile
import unittest
from pathlib import Path


GOOD_SOURCE = (
    'def due_for_review(terminal_epoch, retention_seconds, '
    'now_epoch, hold=False):\n'
    '    if retention_seconds < 0:\n        raise ValueError()\n'
    '    return not hold and now_epoch >= terminal_epoch + retention_seconds\n'
)

BAD_SOURCE = (
    'def due_for_review(terminal_epoch, retention_seconds, '
    'now_epoch, hold=False):\n    return True\n'
)


def _verification_dirs(root):
    verification = root / '.runtime' / 'verification'
    if not verification.exists():
        return []
    return sorted(path for path in verification.iterdir() if path.is_dir())


class GateTests(unittest.TestCase):
    def test_verdict_requires_exact_digest_and_empty_blocking_list(self):
        from agent_coop.gates import check_verdict
        good = {'subject_digest': 'a' * 64, 'verdict': 'PASS', 'blocking': []}
        check_verdict(good, 'a' * 64)
        for patch in ({'subject_digest': 'b' * 64}, {'blocking': ['unresolved']},
                      {'blocking': ''}, {'verdict': 'CHANGES_REQUESTED'}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                check_verdict(good | patch, 'a' * 64)

    def test_verdict_rejects_non_object_result(self):
        from agent_coop.gates import check_verdict
        for bad in ('PASS', ['subject_digest'], None, 42):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                check_verdict(bad, 'a' * 64)

    def test_verifier_checks_boundary_hold_and_negative_retention(self):
        from agent_coop.checks import validate_feature
        from agent_coop.paths import create_root
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            source = root / 'workspace' / 'feature.py'
            source.write_text(
                'def due_for_review(terminal_epoch, retention_seconds, '
                'now_epoch, hold=False):\n    return True\n', encoding='utf-8',
            )
            with self.assertRaises(Exception):
                validate_feature(root)
            source.write_text(
                'def due_for_review(terminal_epoch, retention_seconds, '
                'now_epoch, hold=False):\n'
                '    if retention_seconds < 0:\n        raise ValueError()\n'
                '    return not hold and now_epoch >= terminal_epoch + retention_seconds\n',
                encoding='utf-8',
            )
            result = validate_feature(root)
            self.assertTrue(result['passed'])
            self.assertGreaterEqual(result['cases'], 7)


class ValidateFeatureIsolationTests(unittest.TestCase):
    def _write_source(self, root, text):
        (root / 'workspace' / 'feature.py').write_text(text, encoding='utf-8')

    def _call(self, root, expect_failure):
        from agent_coop.checks import validate_feature
        if expect_failure:
            with self.assertRaises(Exception):
                validate_feature(root)
            return None
        return validate_feature(root)

    def test_failure_then_success_uses_distinct_directories(self):
        from agent_coop.paths import create_root
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            self._write_source(root, BAD_SOURCE)
            self._call(root, expect_failure=True)
            failed = _verification_dirs(root)[0]
            failed_stdout = (failed / 'stdout.log').read_bytes()
            failed_stderr = (failed / 'stderr.log').read_bytes()
            self.assertTrue(failed_stderr)
            self._write_source(root, GOOD_SOURCE)
            result = self._call(root, expect_failure=False)
            self.assertTrue(result['passed'])
            dirs = _verification_dirs(root)
            self.assertEqual(len(dirs), 2)
            self.assertEqual(len({d for d in dirs}), 2)
            self.assertEqual((failed / 'stdout.log').read_bytes(), failed_stdout)
            self.assertEqual((failed / 'stderr.log').read_bytes(), failed_stderr)
            success = next(d for d in dirs if d != failed)
            self.assertEqual(
                json.loads((success / 'stdout.log').read_text(encoding='utf-8')),
                {'passed': True, 'cases': 7})

    def test_success_then_success_keeps_prior_output_bytes(self):
        from agent_coop.paths import create_root
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            self._write_source(root, GOOD_SOURCE)
            self.assertTrue(self._call(root, expect_failure=False)['passed'])
            first = _verification_dirs(root)[0]
            first_stdout = (first / 'stdout.log').read_bytes()
            first_stderr = (first / 'stderr.log').read_bytes()
            self.assertTrue(self._call(root, expect_failure=False)['passed'])
            dirs = _verification_dirs(root)
            self.assertEqual(len(dirs), 2)
            self.assertEqual(len({d for d in dirs}), 2)
            self.assertEqual((first / 'stdout.log').read_bytes(), first_stdout)
            self.assertEqual((first / 'stderr.log').read_bytes(), first_stderr)

    def test_failure_then_failure_retains_each_stderr(self):
        from agent_coop.paths import create_root
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            self._write_source(root, BAD_SOURCE)
            self._call(root, expect_failure=True)
            self._call(root, expect_failure=True)
            dirs = _verification_dirs(root)
            self.assertEqual(len(dirs), 2)
            self.assertEqual(len({d for d in dirs}), 2)
            for path in dirs:
                stderr = (path / 'stderr.log').read_bytes()
                self.assertTrue(stderr)
                self.assertTrue((path / 'stdout.log').exists())

    def test_same_source_repeated_allocates_independent_directories(self):
        from agent_coop.paths import create_root
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            self._write_source(root, GOOD_SOURCE)
            for _ in range(3):
                self.assertTrue(self._call(root, expect_failure=False)['passed'])
            dirs = _verification_dirs(root)
            self.assertEqual(len(dirs), 3)
            self.assertEqual(len({d for d in dirs}), 3)
            outputs = {(d / 'stdout.log').read_bytes() for d in dirs}
            self.assertEqual(len(outputs), 1)

    def test_concurrent_calls_allocate_distinct_directories(self):
        from concurrent.futures import ThreadPoolExecutor
        from agent_coop.checks import validate_feature
        from agent_coop.paths import create_root
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            self._write_source(root, GOOD_SOURCE)
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = list(pool.map(
                    lambda _: validate_feature(root), range(4)))
            self.assertTrue(all(r['passed'] for r in results))
            dirs = _verification_dirs(root)
            self.assertEqual(len(dirs), 4)
            self.assertEqual(len({d for d in dirs}), 4)
            for path in dirs:
                self.assertEqual(
                    json.loads((path / 'stdout.log').read_text(encoding='utf-8')),
                    {'passed': True, 'cases': 7})


if __name__ == '__main__':
    unittest.main()
