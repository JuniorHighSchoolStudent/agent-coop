"""本地和 CI 共用的仓库验证入口。"""
import ast
import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote


def source_limits(root):
    failures, targets = [], []
    for directory in ('agent_coop', 'tests'):
        for path in sorted((root / directory).glob('*.py')):
            source = path.read_text(encoding='utf-8-sig')
            lines = len(source.splitlines())
            tree = ast.parse(source, filename=str(path))
            if lines > 500:
                failures.append(f'{path.relative_to(root)}: {lines} lines > 500')
            elif lines > 300:
                targets.append(f'{path.relative_to(root)}: {lines} lines > target 300')
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    size = node.end_lineno - node.lineno + 1
                    if size > 80:
                        failures.append(f'{path.name}:{node.lineno} {node.name}: {size} > 80')
                    elif size > 40:
                        targets.append(f'{path.name}:{node.lineno} {node.name}: {size} > target 40')
    return failures, targets


def documentation(root):
    failures, count = [], 0
    for path in root.rglob('*.md'):
        if any(part.startswith('.') for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding='utf-8-sig')
        for raw in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', text):
            target = raw.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            target = unquote(target)
            count += 1
            if not (path.parent / target).exists():
                failures.append(f'{path.relative_to(root)}: missing link {target}')
    return failures, count


def verify():
    root = Path(__file__).resolve().parent.parent
    suite = unittest.defaultTestLoader.discover(str(root / 'tests'), top_level_dir=str(root))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    failures, targets = source_limits(root)
    links, count = documentation(root)
    failures.extend(links)
    diff = subprocess.run(['git', 'diff', '--check'], cwd=root, capture_output=True, text=True)
    if diff.returncode:
        failures.append(diff.stdout + diff.stderr)
    for message in targets:
        print(f'REVIEW TARGET: {message}')
    for message in failures:
        print(f'FAIL: {message}')
    print(f'Checked {count} local Markdown links; anchors/remote URLs require scoped review.')
    return 0 if result.wasSuccessful() and not failures else 1
