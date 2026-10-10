"""显式生命周期入口；状态权威仅为 Store。"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path


def parser():
    root = argparse.ArgumentParser(description='Agent Coop 隔离协作样例')
    commands = root.add_subparsers(dest='command', required=True)
    for name in ('init', 'run', 'status', 'pause', 'resume', 'serve'):
        command = commands.add_parser(name)
        command.add_argument('root', type=Path)
        if name == 'init':
            command.add_argument('--profiles', type=Path, required=True)
        elif name == 'run':
            command.add_argument('--max-steps', type=int)
        elif name == 'serve':
            command.add_argument('--port', type=int, default=8765)
    commands.add_parser('verify')
    return root


def _validate_args(args):
    if args.command == 'run' and args.max_steps is not None and args.max_steps < 0:
        raise ValueError('--max-steps must be non-negative')
    if args.command == 'serve' and not 0 <= args.port <= 65535:
        raise ValueError('--port must be between 0 and 65535')


def execute(args):
    if args.command == 'verify':
        from .verification import verify
        return verify()
    _validate_args(args)
    if args.command == 'init':
        from .sample import initialize
        profiles = json.loads(args.profiles.read_text(encoding='utf-8-sig'))
        state = initialize(args.root, profiles)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    from .store import Store
    from .paths import checked
    checked(args.root, '.runtime/state.sqlite')
    store = Store(args.root)
    if args.command == 'run':
        from .runner import Runner
        from .sample import handlers
        Runner(args.root, handlers(args.root)).run(max_steps=args.max_steps)
    elif args.command == 'pause':
        store.pause()
    elif args.command == 'resume':
        store.resume()
    elif args.command == 'serve':
        from .web import serve
        serve(args.root, args.port)
    state = store.read()
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 1 if state['phase'] in ('blocked', 'reconciliation_required') else 0


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = execute(args)
        return result if isinstance(result, int) else 0
    except (ValueError, OSError, RuntimeError, KeyError, sqlite3.Error) as error:
        print(f'agent-coop: {error}', file=sys.stderr)
        return 2
