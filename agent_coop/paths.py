"""隔离样例的路径守卫：根目录创建、相对路径检查、摘要与原子 JSON 写入。"""
import hashlib
import json
import os
import tempfile
from pathlib import Path, PureWindowsPath

MARKER = '.agent-coop-sample'
_SUBDIRS = ('.runtime', 'workspace', 'evidence', 'archives', 'backups', 'scratch')


def _is_reparse_point(path):
    """path（经 lstat）是否为符号链接或 Windows 重解析点（junction 等）。"""
    try:
        if path.is_symlink():
            return True
    except OSError:
        return False
    if os.name == 'nt':
        try:
            attrs = os.lstat(path).st_file_attributes
        except (OSError, AttributeError):
            return False
        return bool(attrs & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    return False


def _require_clean_root(root):
    if not root.is_absolute():
        raise ValueError('root must be absolute')
    if _is_reparse_point(root):
        raise ValueError('root must not be a symlink or junction')
    if not (root / MARKER).exists():
        raise ValueError('root marker missing')


def create_root(path):
    target = Path(path).absolute()
    if target.exists():
        if not target.is_dir():
            raise ValueError('target exists and is not a directory')
        if any(target.iterdir()):
            raise ValueError('directory is not empty')
    else:
        target.mkdir(parents=True)
    (target / MARKER).write_text('agent-coop-sample\n', encoding='utf-8')
    for directory in _SUBDIRS:
        (target / directory).mkdir(exist_ok=True)
    return target


def checked(root, relative):
    root = Path(root).absolute()
    _require_clean_root(root)

    text = os.fspath(relative)
    if not text:
        raise ValueError('empty path rejected')
    if PureWindowsPath(text).drive:
        raise ValueError('drive-letter path rejected')
    rel = Path(text)
    if rel.is_absolute():
        raise ValueError('absolute path rejected')
    parts = rel.parts
    if not parts or '..' in parts:
        raise ValueError('dot or parent traversal rejected')

    target = root.joinpath(*parts)
    current = root
    for part in parts:
        current = current / part
        if _is_reparse_point(current):
            raise ValueError(f'symlink or junction in path: {part}')
        if not current.exists():
            break
    return target


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path).absolute()
    if _is_reparse_point(path):
        raise ValueError('refusing to write through symlink or junction')
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(',', ':')).encode('utf-8')
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + '.',
                               suffix='.tmp')
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
