"""verification 门禁的独立失败用例；构造临时违规源/文档，验证 source_limits 与 documentation 确实检出。"""
import tempfile
import unittest
from pathlib import Path


class SourceLimitsGateTests(unittest.TestCase):
    def test_flags_file_exceeding_hard_line_limit(self):
        from agent_coop.verification import source_limits
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'agent_coop').mkdir()
            source = '\n'.join('# padding' for _ in range(501)) + '\n'
            (root / 'agent_coop' / 'oversized.py').write_text(source, encoding='utf-8')
            failures, _targets = source_limits(root)
            self.assertTrue(any('> 500' in message for message in failures))

    def test_flags_function_exceeding_hard_line_limit(self):
        from agent_coop.verification import source_limits
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'agent_coop').mkdir()
            source = 'def oversized():\n' + '\n'.join('    pass' for _ in range(84)) + '\n'
            (root / 'agent_coop' / 'oversized.py').write_text(source, encoding='utf-8')
            failures, _targets = source_limits(root)
            self.assertTrue(any('> 80' in message for message in failures))

    def test_reports_moderate_oversize_as_review_target_not_failure(self):
        from agent_coop.verification import source_limits
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'agent_coop').mkdir()
            source = '\n'.join('# padding' for _ in range(301)) + '\n'
            (root / 'agent_coop' / 'moderate.py').write_text(source, encoding='utf-8')
            failures, targets = source_limits(root)
            self.assertFalse(any('> 500' in message for message in failures))
            self.assertTrue(any('> target 300' in message for message in targets))


class DocumentationGateTests(unittest.TestCase):
    def test_flags_missing_relative_link(self):
        from agent_coop.verification import documentation
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text(
                '[missing](does-not-exist.md)\n', encoding='utf-8')
            failures, _count = documentation(root)
            self.assertTrue(any('missing link' in message for message in failures))

    def test_ignores_remote_urls_and_existing_targets(self):
        from agent_coop.verification import documentation
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text(
                '[remote](https://example.com/x)\n[local](present.md)\n', encoding='utf-8')
            (root / 'present.md').write_text('# present\n', encoding='utf-8')
            failures, count = documentation(root)
            self.assertFalse(failures)
            self.assertEqual(count, 1)


if __name__ == '__main__':
    unittest.main()
