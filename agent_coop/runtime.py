"""Runtime 子进程边界：有界墙钟/输出、进程树终止与 invoke 收据。"""
import hashlib
import os
import subprocess
import threading
import time
from pathlib import Path

from . import adapters


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _validate_budget(timeout_seconds, output_limit_bytes):
    if (not isinstance(timeout_seconds, (int, float))
            or isinstance(timeout_seconds, bool)
            or not 0 < timeout_seconds < float('inf')):
        raise ValueError('timeout_seconds must be a positive finite number')
    if (not isinstance(output_limit_bytes, int)
            or isinstance(output_limit_bytes, bool)
            or output_limit_bytes <= 0):
        raise ValueError('output_limit_bytes must be a positive integer')


def _resolve_log_dir(cwd, log_dir):
    from .paths import checked
    root = Path(cwd).absolute()
    runtime_base = Path(checked(root, '.runtime'))
    provided = Path(log_dir)
    if not provided.is_absolute():
        provided = root / provided
    try:
        relative = provided.relative_to(root)
    except ValueError:
        raise ValueError('log_dir must be inside the isolation root')
    target = Path(checked(root, relative))
    if target != runtime_base and runtime_base not in target.parents:
        raise ValueError(
            'log_dir must be inside the isolation root .runtime')
    return target


def run_bounded(argv, cwd, log_dir, timeout_seconds, output_limit_bytes,
                env=None):
    _validate_budget(timeout_seconds, output_limit_bytes)
    log_path = _resolve_log_dir(cwd, log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()

    popen_kwargs = {}
    if os.name != 'nt':
        popen_kwargs['start_new_session'] = True
    if env is not None:
        popen_kwargs['env'] = env
    proc = subprocess.Popen(
        argv, cwd=str(cwd), shell=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, **popen_kwargs,
    )
    out_bytes, err_bytes, failure = _collect(
        proc, timeout_seconds, output_limit_bytes)
    wall = time.monotonic() - start
    _write_logs(log_path, out_bytes, err_bytes)
    if failure:
        raise RuntimeError(failure)
    return {
        'stdout': out_bytes.decode('utf-8'),
        'stderr': err_bytes.decode('utf-8'),
        'exit_code': proc.returncode,
        'wall_seconds': wall,
        'stdout_sha256': hashlib.sha256(out_bytes).hexdigest(),
        'stderr_sha256': hashlib.sha256(err_bytes).hexdigest(),
    }


def _collect(proc, timeout_seconds, output_limit_bytes):
    out = bytearray()
    err = bytearray()
    lock = threading.Lock()
    total = [0]
    exceeded = [False]
    reader_errors = []

    out_thread = threading.Thread(
        target=_pump_stream,
        args=(proc.stdout, out, lock, total, exceeded, reader_errors,
              output_limit_bytes), daemon=True)
    err_thread = threading.Thread(
        target=_pump_stream,
        args=(proc.stderr, err, lock, total, exceeded, reader_errors,
              output_limit_bytes), daemon=True)
    out_thread.start()
    err_thread.start()

    timed_out, parent_alive, readers_alive = _supervise(
        proc, out_thread, err_thread, exceeded, timeout_seconds)

    failure = _classify_failure(
        reader_errors, exceeded[0], parent_alive, timed_out, readers_alive,
        proc.returncode)

    _close(proc.stdout)
    _close(proc.stderr)
    return bytes(out), bytes(err), failure


def _pump_stream(stream, buf, lock, total, exceeded, reader_errors,
                 output_limit_bytes):
    try:
        while True:
            chunk = stream.read(65536)
            if not chunk:
                return
            with lock:
                if exceeded[0]:
                    return
                room = output_limit_bytes - total[0]
                if room <= 0:
                    exceeded[0] = True
                    return
                take = chunk[:room]
                buf.extend(take)
                total[0] += len(take)
                if len(chunk) > room:
                    exceeded[0] = True
                    return
    except Exception as exc:
        reader_errors.append(exc)


def _supervise(proc, out_thread, err_thread, exceeded, timeout_seconds):
    timed_out = False
    deadline = time.monotonic() + timeout_seconds
    while True:
        parent_alive = proc.poll() is None
        readers_alive = out_thread.is_alive() or err_thread.is_alive()
        if exceeded[0]:
            break
        if not parent_alive and not readers_alive:
            break
        if time.monotonic() >= deadline:
            timed_out = True
            break
        time.sleep(0.02)

    if proc.poll() is None:
        _terminate_tree(proc)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass
    parent_alive = proc.poll() is None

    grace_end = time.monotonic() + 5
    while (out_thread.is_alive() or err_thread.is_alive()) \
            and time.monotonic() < grace_end:
        time.sleep(0.02)
    readers_alive = out_thread.is_alive() or err_thread.is_alive()

    return timed_out, parent_alive, readers_alive


def _classify_failure(reader_errors, exceeded, parent_alive, timed_out,
                      readers_alive, returncode):
    if reader_errors:
        return f'output reader error: {reader_errors[0]}'
    if exceeded:
        return 'output limit exceeded'
    if parent_alive:
        return 'termination failed (process still alive)'
    if timed_out or readers_alive:
        if readers_alive and returncode is not None:
            return ('timeout exceeded (parent exited, '
                    'output readers still alive)')
        return 'timeout exceeded'
    if returncode != 0:
        return f'exit code {returncode}'
    return None


def _terminate_tree(proc):
    if proc.poll() is not None:
        return
    if os.name == 'nt':
        try:
            subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'],
                           capture_output=True, timeout=15, shell=False)
        except Exception:
            pass
    else:
        try:
            import signal
            os.killpg(proc.pid, signal.SIGKILL)
        except Exception:
            pass
    try:
        proc.kill()
    except Exception:
        pass


def _close(pipe):
    try:
        pipe.close()
    except Exception:
        pass


def _write_logs(log_dir, out_bytes, err_bytes):
    log_dir = Path(log_dir)
    stdout_path = log_dir / 'stdout.log'
    stderr_path = log_dir / 'stderr.log'
    if stdout_path.exists() or stderr_path.exists():
        raise ValueError(
            f'refusing to overwrite existing log files in {log_dir}')
    stdout_path.write_bytes(out_bytes)
    stderr_path.write_bytes(err_bytes)


def invoke(profile, prompt, cwd, log_dir, session_id):
    _verify_hashes(profile)
    _verify_cwd(profile, cwd)
    argv = adapters.command(profile, prompt, session_id)
    env = _build_env(profile['permissions']['environment'])
    bounded = run_bounded(argv, cwd, log_dir, profile['timeout_seconds'],
                          profile['output_limit_bytes'], env=env)
    receipt = adapters.parse(profile, bounded['stdout'], session_id)
    receipt['exit_code'] = bounded['exit_code']
    receipt['wall_seconds'] = bounded['wall_seconds']
    receipt['stdout_sha256'] = bounded['stdout_sha256']
    receipt['stderr_sha256'] = bounded['stderr_sha256']
    return receipt


def _verify_cwd(profile, cwd):
    permissions = profile.get('permissions')
    if not isinstance(permissions, dict):
        raise ValueError('permissions are required')
    root = permissions.get('root')
    if not isinstance(root, str) or not root:
        raise ValueError('permissions.root is required')
    actual = adapters.canonical_path(cwd)
    if root != actual:
        raise ValueError(f'cwd does not match permissions.root: {actual} != {root}')


def _build_env(environment):
    if not isinstance(environment, dict):
        raise ValueError('permissions.environment must be an object')
    if set(environment) != {'inherit', 'set'}:
        raise ValueError(
            'permissions.environment must contain exactly inherit and set')
    inherit = environment['inherit']
    if not isinstance(inherit, (list, tuple)):
        raise ValueError('environment.inherit must be a list')
    seen = {}
    for name in inherit:
        if not isinstance(name, str) or not name:
            raise ValueError(
                'environment.inherit names must be non-empty strings')
        key = name.casefold()
        if key in seen:
            raise ValueError(
                f'duplicate or case-ambiguous inherit name: {name}')
        seen[key] = name
    set_values = environment['set']
    if not isinstance(set_values, dict):
        raise ValueError('environment.set must be an object')
    for key, value in set_values.items():
        if not isinstance(key, str) or not key:
            raise ValueError('environment.set keys must be non-empty strings')
        if not isinstance(value, str):
            raise ValueError('environment.set values must be strings')
    env = {}
    for name in inherit:
        if name in os.environ:
            env[name] = os.environ[name]
    env.update(set_values)
    if not env.get('PATH'):
        raise ValueError('PATH must be non-empty in the subprocess environment')
    if os.name == 'nt' and not env.get('SYSTEMROOT'):
        raise ValueError('SYSTEMROOT must be non-empty on Windows')
    return env


def _verify_hashes(profile):
    _verify_file_hash(profile.get('executable'),
                      profile.get('executable_sha256'), 'executable')
    _verify_file_hash(profile.get('entry'),
                      profile.get('entry_sha256'), 'entry')
    if profile.get('adapter') == 'kimi':
        _verify_file_hash(profile.get('agent_file'),
                          profile.get('agent_file_sha256'), 'agent_file')


def _verify_file_hash(path, expected, label):
    if not path:
        raise ValueError(f'{label} is required')
    if not expected:
        raise ValueError(f'{label}_sha256 is required')
    resolved = Path(path)
    if not resolved.is_absolute():
        raise ValueError(f'{label} must be an absolute path: {path}')
    if not resolved.is_file():
        raise ValueError(f'{label} is not a regular file: {path}')
    actual = _sha256(resolved)
    if actual != expected:
        raise ValueError(f'{label} sha256 mismatch: {actual} != {expected}')
