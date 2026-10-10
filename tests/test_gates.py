"""门禁不采信 PASS 文字或旧候选。"""
import tempfile
import unittest
from pathlib import Path


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


if __name__ == '__main__':
    unittest.main()
