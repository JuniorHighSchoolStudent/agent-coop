"""paths 路径守卫合同测试（独立于 Store）。"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_coop import paths


def make_link(link_path, target_path):
    """Windows 用 junction，其余用目录符号链接；返回跳过原因或 None。"""
    if sys.platform == 'win32':
        proc = subprocess.run(
            ['cmd', '/c', 'mklink', '/J', str(link_path), str(target_path)],
            capture_output=True, text=True)
        return None if proc.returncode == 0 else f'mklink /J 不可用: {proc.stderr.strip()}'
    try:
        Path(link_path).symlink_to(target_path, target_is_directory=True)
    except OSError as exc:
        return f'symlink 不可用: {exc}'
    return None


def remove_link(path):
    """仅移除 junction/符号链接自身，不递归其目标。"""
    path = Path(path)
    for cleaner in (os.rmdir, os.unlink):
        try:
            cleaner(path)
            return
        except OSError:
            continue


class PathsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def make_root(self):
        return paths.create_root(self.tmp / 'sample')

    def test_create_root_layout_marker_and_empty_dir(self):
        target = self.tmp / 'sample'
        target.mkdir()  # 预先存在的空目录也应接受
        self.assertEqual(paths.create_root(target), target)
        self.assertTrue((target / '.agent-coop-sample').exists())
        for directory in ('.runtime', 'workspace', 'evidence',
                          'archives', 'backups', 'scratch'):
            self.assertTrue((target / directory).is_dir(), directory)

    def test_create_root_rejects_non_empty(self):
        target = self.tmp / 'sample'
        target.mkdir()
        keep = target / 'keep.txt'
        keep.write_text('keep', encoding='utf-8')
        with self.assertRaises(ValueError):
            paths.create_root(target)
        self.assertEqual(keep.read_text(encoding='utf-8'), 'keep')
        self.assertFalse((target / '.agent-coop-sample').exists())

    def test_checked_rejects_absolute_and_bad_relative(self):
        root = self.make_root()
        cases = ('', '.', '..', '../outside', 'a/../../b',
                 str(root / 'workspace'))
        for relative in cases:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                paths.checked(root, relative)

    def test_checked_rejects_symlink(self):
        root = self.make_root()
        outside = self.tmp / 'outside'
        outside.mkdir()
        (outside / 'x.txt').write_text('x', encoding='utf-8')
        try:
            (root / 'link.txt').symlink_to(outside / 'x.txt')
            (root / 'dirlink').symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f'symlink 不可用: {exc}')
        for relative in ('link.txt', 'dirlink', 'dirlink/x.txt'):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                paths.checked(root, relative)

    @unittest.skipUnless(sys.platform == 'win32', 'junction 仅 Windows')
    def test_checked_rejects_junction(self):
        import subprocess
        root = self.make_root()
        target = self.tmp / 'real'
        target.mkdir()
        proc = subprocess.run(
            ['cmd', '/c', 'mklink', '/J', str(root / 'junction'), str(target)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            self.skipTest(f'mklink /J 不可用: {proc.stderr.strip()}')
        with self.assertRaises(ValueError):
            paths.checked(root, 'junction')

    def test_checked_requires_root_marker(self):
        plain = self.tmp / 'plain'
        plain.mkdir()
        with self.assertRaises(ValueError):
            paths.checked(plain, 'anything.txt')

    def test_checked_returns_path_within_root(self):
        root = self.make_root()
        self.assertEqual(paths.checked(root, 'workspace/feature.py'),
                         root / 'workspace' / 'feature.py')

    def test_digest_matches_sha256(self):
        path = self.tmp / 'data.txt'
        path.write_bytes(b'hello world\n')
        self.assertEqual(paths.digest(path),
                         hashlib.sha256(b'hello world\n').hexdigest())

    def test_write_json_roundtrip(self):
        path = self.tmp / 'out.json'
        value = {'a': [1, 2], 'b': {'c': '中文'}}
        paths.write_json(path, value)
        self.assertEqual(json.loads(path.read_text(encoding='utf-8')), value)

    def test_create_root_rejects_junction_root(self):
        outside = self.tmp / 'outside'
        outside.mkdir()
        junction = self.tmp / 'junction'
        reason = make_link(junction, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, junction)
        with self.assertRaises(ValueError):
            paths.create_root(junction)
        self.assertFalse((outside / '.agent-coop-sample').exists())

    def test_create_root_rejects_junction_ancestor(self):
        outside = self.tmp / 'outside'
        outside.mkdir()
        junction = self.tmp / 'junction'
        reason = make_link(junction, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, junction)
        with self.assertRaises(ValueError):
            paths.create_root(junction / 'child')
        self.assertFalse((outside / 'child').exists())

    def test_checked_rejects_junction_ancestor(self):
        outside = self.tmp / 'outside'
        (outside / 'sub').mkdir(parents=True)
        (outside / 'sub' / '.agent-coop-sample').write_text('x', encoding='utf-8')
        junction = self.tmp / 'junction'
        reason = make_link(junction, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, junction)
        with self.assertRaises(ValueError):
            paths.checked(junction / 'sub', 'workspace/feature.py')

    def test_write_json_rejects_junction_parent(self):
        outside = self.tmp / 'outside'
        outside.mkdir()
        junction = self.tmp / 'junction'
        reason = make_link(junction, outside)
        if reason:
            self.skipTest(reason)
        self.addCleanup(remove_link, junction)
        with self.assertRaises(ValueError):
            paths.write_json(junction / 'out.json', {'k': 1})
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
