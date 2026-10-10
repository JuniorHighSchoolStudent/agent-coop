"""Store：SQLite 单写权威、不可变 revision 事件与发布投影。"""
import hashlib
import json
import os
import sqlite3
import threading
from pathlib import Path

# update 不得改写的权威内部字段；phase/calls_used/paused/data/error 仍可由可信 handler 更新。
_PROTECTED_UPDATE_FIELDS = frozenset({
    'revision', 'schema', 'config_digest', 'config', 'steps', 'current_step',
})


def canonical_digest(value):
    """唯一规范摘要：sorted/compact/ensure_ascii=False UTF-8 的 SHA256。"""
    text = json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class PausedError(RuntimeError):
    """状态已暂停，begin 拒绝派发新步骤；runner 据此返回最新状态而不记 failed。"""


_held = set()
_held_lock = threading.Lock()


class file_lock:
    """跨平台文件锁；非阻塞模式下若已持有则立即抛 BlockingIOError。"""

    def __init__(self, path, blocking=True):
        self.path = str(Path(path).resolve())
        self.blocking = blocking
        self._file = None
        self._acquired = False

    def __enter__(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with _held_lock:
            if not self.blocking and self.path in _held:
                raise BlockingIOError(13, 'lock already held', self.path)
        self._file = open(self.path, 'a+b')
        if os.name == 'nt':
            import msvcrt
            self._file.seek(0, 2)
            if self._file.tell() == 0:
                self._file.write(b'\0')
                self._file.flush()
            self._file.seek(0)
            mode = msvcrt.LK_LOCK if self.blocking else msvcrt.LK_NBLCK
            try:
                msvcrt.locking(self._file.fileno(), mode, 1)
            except OSError as exc:
                self._file.close()
                self._file = None
                if not self.blocking:
                    raise BlockingIOError(
                        exc.errno, 'lock busy', self.path) from exc
                raise
        else:
            import fcntl
            op = fcntl.LOCK_EX
            if not self.blocking:
                op |= fcntl.LOCK_NB
            try:
                fcntl.flock(self._file.fileno(), op)
            except OSError:
                self._file.close()
                self._file = None
                raise
        with _held_lock:
            _held.add(self.path)
        self._acquired = True
        return self

    def __exit__(self, *exc):
        if self._file is not None:
            if os.name == 'nt':
                import msvcrt
                self._file.seek(0)
                msvcrt.locking(self._file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
            self._file.close()
            self._file = None
        if self._acquired:
            with _held_lock:
                _held.discard(self.path)
            self._acquired = False
        return False


class Store:
    """单个 SQLite 权威：一行 JSON 状态 + 同事务不可变 revision 事件表。"""

    def __init__(self, root):
        self.root = Path(root)
        self.runtime_dir = self.root / '.runtime'
        self.db_path = self.runtime_dir / 'state.sqlite'
        self.outbox_dir = self.runtime_dir / 'outbox'
        self.publish_lock_path = self.runtime_dir / 'publish.lock'

    def _connect(self):
        conn = sqlite3.connect(str(self.db_path), timeout=30)
        conn.isolation_level = None
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self, conn):
        conn.execute(
            'CREATE TABLE IF NOT EXISTS state ('
            'id INTEGER PRIMARY KEY CHECK (id = 1), '
            'revision INTEGER NOT NULL, '
            'snapshot TEXT NOT NULL)'
        )
        conn.execute(
            'CREATE TABLE IF NOT EXISTS events ('
            'revision INTEGER PRIMARY KEY, '
            'snapshot TEXT NOT NULL)'
        )

    def _initial_state(self, config, steps):
        return {
            'schema': 1,
            'revision': 0,
            'config': config,
            'config_digest': canonical_digest(config),
            'phase': 'ready',
            'paused': False,
            'current_step': None,
            'steps': [{'name': name, 'status': 'pending'} for name in steps],
            'data': {},
            'error': None,
            'calls_used': 0,
        }

    def _snapshot_text(self, state):
        return json.dumps(state, sort_keys=True, separators=(',', ':'),
                          ensure_ascii=False)

    def _record(self, conn, state):
        revision = state['revision']
        snapshot = self._snapshot_text(state)
        conn.execute(
            'INSERT OR REPLACE INTO state (id, revision, snapshot) '
            'VALUES (1, ?, ?)', (revision, snapshot),
        )
        conn.execute(
            'INSERT INTO events (revision, snapshot) VALUES (?, ?)',
            (revision, snapshot),
        )

    def _load_state(self, conn):
        row = conn.execute('SELECT snapshot FROM state WHERE id = 1').fetchone()
        if row is None:
            raise RuntimeError('store not initialized')
        return json.loads(row['snapshot'])

    def _find_step(self, state, name):
        for step in state['steps']:
            if step['name'] == name:
                return step
        raise KeyError(f'unknown step {name}')

    def _rollback(self, conn):
        try:
            conn.execute('ROLLBACK')
        except sqlite3.Error:
            pass

    def _mutate(self, apply, publish=True):
        conn = self._connect()
        try:
            self._ensure_schema(conn)
            conn.execute('BEGIN IMMEDIATE')
            state = self._load_state(conn)
            apply(state)
            state['revision'] += 1
            self._record(conn, state)
            conn.execute('COMMIT')
        except BaseException:
            self._rollback(conn)
            raise
        finally:
            conn.close()
        if publish:
            try:
                self.publish()
            except BlockingIOError:
                pass  # 发布锁忙：仅受控延后，事件已落 events outbox，后续 publish 重放
        return state

    @staticmethod
    def _validate_steps(steps):
        if not isinstance(steps, (list, tuple)) or not steps:
            raise ValueError('steps must be a non-empty sequence')
        names = []
        for name in steps:
            if not isinstance(name, str) or not name:
                raise ValueError('step names must be non-empty strings')
            names.append(name)
        if len(set(names)) != len(names):
            raise ValueError('step names must be unique')
        return names

    def initialize(self, config, steps):
        if not isinstance(config, dict):
            raise TypeError('config must be a dict')
        names = self._validate_steps(steps)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        conn = self._connect()
        try:
            self._ensure_schema(conn)
            conn.execute('BEGIN IMMEDIATE')
            row = conn.execute('SELECT id FROM state WHERE id = 1').fetchone()
            if row is not None:
                raise RuntimeError('store already initialized; refusing to reset')
            state = self._initial_state(config, names)
            self._record(conn, state)
            conn.execute('COMMIT')
        except BaseException:
            self._rollback(conn)
            raise
        finally:
            conn.close()
        try:
            self.publish()
        except BlockingIOError:
            pass
        return state

    def read(self):
        if not self.db_path.exists():
            raise RuntimeError('store not initialized')
        conn = self._connect()
        try:
            try:
                row = conn.execute(
                    'SELECT snapshot FROM state WHERE id = 1').fetchone()
            except sqlite3.OperationalError:
                raise RuntimeError('store not initialized')
            if row is None:
                raise RuntimeError('store not initialized')
            return json.loads(row['snapshot'])
        finally:
            conn.close()

    def update(self, **changes):
        for key in _PROTECTED_UPDATE_FIELDS:
            if key in changes:
                raise ValueError(f'field {key} is internally managed')

        def apply(state):
            for key, value in changes.items():
                if key == 'data':
                    merged = dict(state.get('data') or {})
                    merged.update(value or {})
                    state['data'] = merged
                else:
                    state[key] = value
        return self._mutate(apply)

    def begin(self, step):
        def apply(state):
            if state['paused']:
                raise PausedError('paused; step not dispatched')
            if state['phase'] in ('blocked', 'reconciliation_required'):
                raise ValueError(
                    f'cannot begin from phase {state["phase"]}')
            if state['current_step'] is not None:
                raise ValueError(
                    f'current_step {state["current_step"]} still running')
            if any(s['status'] == 'running' for s in state['steps']):
                raise ValueError('residual running step; reconcile first')
            entry = self._find_step(state, step)
            if entry['status'] != 'pending':
                raise ValueError(
                    f'step {step} is {entry["status"]}, not pending')
            entry['status'] = 'running'
            state['current_step'] = step
            state['phase'] = 'running'
            state['error'] = None
        return self._mutate(apply)

    def finish(self, step, updates=None):
        def apply(state):
            entry = self._find_step(state, step)
            if entry['status'] != 'running':
                raise ValueError(
                    f'step {step} is {entry["status"]}, not running')
            entry['status'] = 'done'
            data = dict(state.get('data') or {})
            data.update(updates or {})
            state['data'] = data
            state['current_step'] = None
            state['error'] = None
            if all(s['status'] == 'done' for s in state['steps']):
                state['phase'] = 'complete'
            elif state['paused']:
                state['phase'] = 'paused'
            else:
                state['phase'] = 'ready'
        return self._mutate(apply)

    def fail(self, step, message):
        def apply(state):
            entry = self._find_step(state, step)
            entry['status'] = 'failed'
            state['current_step'] = None
            state['phase'] = 'blocked'
            state['error'] = message
        return self._mutate(apply)

    def pause(self):
        def apply(state):
            state['paused'] = True
        # 短事务先持久化暂停；发布锁忙仅延后投影，其它发布异常向上传递。
        return self._mutate(apply)

    def resume(self):
        def apply(state):
            if state['phase'] in ('blocked', 'reconciliation_required'):
                raise ValueError(
                    f'cannot resume from phase {state["phase"]}')
            if any(s['status'] == 'failed' for s in state['steps']):
                raise ValueError('cannot resume with failed steps')
            if any(s['status'] == 'running' for s in state['steps']):
                raise ValueError('cannot resume with running steps')
            state['paused'] = False
            if state['phase'] == 'paused':
                state['phase'] = (
                    'complete' if all(s['status'] == 'done'
                                       for s in state['steps'])
                    else 'ready')
        return self._mutate(apply)

    def publish(self):
        """锁内读取最新 DB 一致快照，重放 events outbox 并写投影。"""
        with file_lock(self.publish_lock_path, blocking=False):
            conn = self._connect()
            try:
                conn.execute('BEGIN')
                row = conn.execute(
                    'SELECT snapshot FROM state WHERE id = 1').fetchone()
                if row is None:
                    conn.execute('COMMIT')
                    return
                state = json.loads(row['snapshot'])
                events = conn.execute(
                    'SELECT revision, snapshot FROM events '
                    'ORDER BY revision').fetchall()
                conn.execute('COMMIT')
            except BaseException:
                self._rollback(conn)
                raise
            finally:
                conn.close()
            self.outbox_dir.mkdir(parents=True, exist_ok=True)
            for event in events:
                self._write_outbox_event(event['revision'], event['snapshot'])
            self._write_projection(self.root / 'state.json', state)
            self._write_status(self.root / 'STATUS', state)
        return state

    def _write_outbox_event(self, revision, snapshot):
        path = self.outbox_dir / f'{revision:06d}.json'
        if path.exists():
            existing = path.read_text(encoding='utf-8')
            if existing != snapshot:
                raise RuntimeError(f'outbox event {revision} conflict')
            return
        self._atomic_write(path, snapshot)

    def _write_projection(self, path, state):
        if path.exists():
            try:
                existing = json.loads(path.read_text(encoding='utf-8'))
                if existing.get('revision', -1) > state['revision']:
                    return
            except (ValueError, OSError):
                pass
        self._atomic_write(path, self._snapshot_text(state))

    def _write_status(self, path, state):
        lines = [
            f'revision: {state["revision"]}',
            f'phase: {state["phase"]}',
            f'paused: {state["paused"]}',
            f'current_step: {state["current_step"]}',
            f'error: {state["error"]}',
        ]
        for step in state['steps']:
            lines.append(f'step {step["name"]}: {step["status"]}')
        self._atomic_write(path, '\n'.join(lines) + '\n')

    def _atomic_write(self, path, text):
        tmp = path.with_name(path.name + '.tmp')
        tmp.write_text(text, encoding='utf-8')
        os.replace(tmp, path)
