"""Runner：唯一有界驱动，整轮持非阻塞文件锁，短事务步进。"""
from pathlib import Path

from .store import PausedError, Store, file_lock


class Runner:
    def __init__(self, root, handlers):
        self.root = Path(root)
        self.handlers = handlers

    def run(self, max_steps=None):
        if max_steps is not None and (
                isinstance(max_steps, bool)
                or not isinstance(max_steps, int)
                or max_steps < 0):
            raise ValueError('max_steps must be a non-negative int or None')
        lock_path = self.root / '.runtime' / 'run.lock'
        with file_lock(lock_path, blocking=False):
            return self._run_locked(max_steps)

    def _run_locked(self, max_steps):
        store = Store(self.root)
        state = store.read()
        if any(step['status'] == 'running' for step in state['steps']):
            store.update(phase='reconciliation_required')
            return store.read()
        if state['phase'] in ('blocked', 'reconciliation_required'):
            return state
        executed = 0
        while True:
            state = store.read()
            if state['paused']:
                break
            if max_steps is not None and executed >= max_steps:
                break
            step = self._next_pending(state)
            if step is None:
                break
            name = step['name']
            handler = self.handlers.get(name)
            if handler is None:
                raise ValueError(f'no handler for step {name}')
            try:
                store.begin(name)
            except PausedError:
                return store.read()
            current = store.read()
            try:
                updates = handler(current)
            except Exception as exc:
                store.fail(name, str(exc))
                break
            if not isinstance(updates, dict):
                store.fail(name, 'handler returned non-dict result')
                break
            # finish 先落 DB（done）再发布；发布失败时 done 已持久化并向上传递，
            # 不把已交付 step 记 failed，后继 run 也不重派 done。
            store.finish(name, updates)
            executed += 1
        try:
            store.publish()
        except BlockingIOError:
            pass
        return store.read()

    def _next_pending(self, state):
        for step in state['steps']:
            if step['status'] == 'pending':
                return step
        return None
