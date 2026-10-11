"""CodeBuddy / Kimi 命令构造与 stream-json 协议解析。"""
import json
import os
from pathlib import Path

PERMISSION_SCOPE = 'cli_tool_filter_not_os_sandbox'
_FORBIDDEN_RULE_CHARS = frozenset('*?[](){},!')


def canonical_path(path):
    """原始 reparse 检查后以 resolve(strict=False).as_posix() 作为规范字符串。

    Windows 仅接受本地盘符绝对路径，盘符统一大写，拒绝 UNC 与设备路径；
    其余组件拼写保留 resolve 返回原样，不整体 lower/casefold。
    """
    from .paths import _reject_reparse_chain
    target = Path(path).absolute()
    _reject_reparse_chain(target)
    resolved = target.resolve(strict=False)
    if os.name == 'nt':
        drive = resolved.drive
        if len(drive) != 2 or drive[1] != ':' or not drive[0].isalpha():
            raise ValueError(
                'only local drive-letter absolute Windows paths are supported')
        return drive[0].upper() + ':' + resolved.as_posix()[2:]
    return resolved.as_posix()


def _validate_canonical_field(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError(f'{label} must be a non-empty string')
    if canonical_path(value) != value:
        raise ValueError(f'{label} must be the canonical absolute path: {value!r}')
    return value


def _validate_file_rule(path):
    for char in path:
        if ord(char) < 32 or ord(char) == 127:
            raise ValueError(f'control character in write rule: {ord(char)}')
        if char in _FORBIDDEN_RULE_CHARS:
            raise ValueError(f'forbidden character in write rule: {char!r}')
    return path


def _validate_permissions(profile):
    permissions = profile.get('permissions')
    if not isinstance(permissions, dict):
        raise ValueError('permissions are required')
    if set(permissions) != {'schema', 'scope', 'root', 'write_files',
                            'environment'}:
        raise ValueError(
            'permissions must contain exactly schema, scope, root, '
            'write_files, environment')
    schema = permissions.get('schema')
    if isinstance(schema, bool) or not isinstance(schema, int) or schema != 1:
        raise ValueError('permissions.schema must be the integer 1')
    if permissions.get('scope') != PERMISSION_SCOPE:
        raise ValueError(f'permissions.scope must be {PERMISSION_SCOPE}')
    _validate_canonical_field(permissions.get('root'), 'permissions.root')
    write_files = permissions.get('write_files')
    if not isinstance(write_files, list):
        raise ValueError('permissions.write_files must be a list')
    for path in write_files:
        _validate_canonical_field(path, 'permissions.write_files entry')
        _validate_file_rule(path)
    environment = permissions.get('environment')
    if not isinstance(environment, dict) or set(environment) != {'inherit', 'set'}:
        raise ValueError(
            'permissions.environment must contain exactly inherit and set')
    tools = list(profile.get('tools') or [])
    write_tools = [tool for tool in tools if tool in ('Write', 'Edit')]
    if write_files and set(write_tools) != {'Write', 'Edit'}:
        raise ValueError('write_files require both Write and Edit tools')
    if not write_files and write_tools:
        raise ValueError('read-only profile must not declare write_files')
    return permissions


def command(profile, prompt, session_id):
    adapter = profile['adapter']
    if adapter == 'codebuddy':
        return _codebuddy_command(profile, prompt, session_id)
    if adapter == 'kimi':
        return _kimi_command(profile, prompt)
    raise ValueError(f'unknown adapter {adapter}')


def _codebuddy_command(profile, prompt, session_id):
    max_turns = profile.get('max_turns')
    if not isinstance(max_turns, int) or isinstance(max_turns, bool) \
            or max_turns <= 0:
        raise ValueError('max_turns must be a positive integer')
    tools = list(profile.get('tools') or [])
    permissions = _validate_permissions(profile)
    argv = [
        profile['executable'],
        profile['entry'],
        '-p', prompt,
        '--model', profile['model'],
        '--session-id', session_id,
        '--tools', ','.join(tools),
        '--permission-mode', 'dontAsk',
        '--setting-sources', 'none',
        '--disallowedTools', 'Bash',
        '--disallowedTools', 'PowerShell',
        '--strict-mcp-config',
        '--mcp-config', '{"mcpServers":{}}',
        '--max-turns', str(max_turns),
        '--output-format', 'stream-json',
        '--verbose',
    ]
    for tool in tools:
        if tool in ('Read', 'Glob', 'Grep'):
            argv += ['--allowedTools', tool]
    for path in permissions['write_files']:
        argv += ['--allowedTools', f'Write({path})']
        argv += ['--allowedTools', f'Edit({path})']
    return argv


def _kimi_command(profile, prompt):
    _validate_permissions(profile)
    if profile['permissions']['write_files']:
        raise ValueError('kimi adapter cannot express write_files')
    return [
        profile['executable'],
        profile['entry'],
        '--agent-file', profile['agent_file'],
        '--prompt', prompt,
        '--output-format', 'stream-json',
    ]


def parse(profile, stdout, session_id):
    adapter = profile['adapter']
    if adapter == 'codebuddy':
        return _parse_codebuddy(profile, stdout, session_id)
    if adapter == 'kimi':
        return _parse_kimi(profile, stdout, session_id)
    raise ValueError(f'unknown adapter {adapter}')


def _events(stdout):
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except ValueError as exc:
            raise ValueError(f'invalid JSONL line: {exc}') from exc
        if not isinstance(event, dict):
            raise ValueError('JSONL line is not a json object')
        yield event


def _check_tools(profile, observed):
    allowed = list(profile.get('tools') or [])
    over = [name for name in observed if name not in allowed]
    if over:
        raise ValueError(f'tool outside profile tools: {sorted(set(over))}')


def _tool_summary(observed, tool_errors, tool_errors_unknown):
    return (f'{len(observed)} tools observed, '
            f'{tool_errors} errors, {tool_errors_unknown} unknown')


def _parse_codebuddy(profile, stdout, session_id):
    init = None
    result_event = None
    observed = []
    tool_errors = 0
    tool_errors_unknown = 0
    for event in _events(stdout):
        etype = event.get('type')
        if etype == 'system' and event.get('subtype') == 'init':
            init = event
        elif etype == 'assistant':
            message = event.get('message') or {}
            for item in message.get('content') or []:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    observed.append(item.get('name'))
        elif etype == 'user':
            message = event.get('message') or {}
            for item in message.get('content') or []:
                if isinstance(item, dict) and item.get('type') == 'tool_result':
                    if 'is_error' in item:
                        if item.get('is_error'):
                            tool_errors += 1
                    else:
                        tool_errors_unknown += 1
        elif etype == 'result':
            result_event = event
    if init is None:
        raise ValueError('init event missing')
    actual_model = init.get('model')
    actual_session = init.get('session_id')
    if actual_model != profile.get('model'):
        raise ValueError(f'model mismatch: {actual_model}')
    if actual_session != session_id:
        raise ValueError(f'session mismatch: {actual_session}')
    if result_event is None:
        raise ValueError('result event missing')
    if result_event.get('is_error') is not False:
        raise ValueError('result is_error must be explicitly false')
    result = _result_object(result_event.get('result'))
    _check_tools(profile, observed)
    return {
        'adapter': 'codebuddy',
        'requested_model': profile.get('model'),
        'actual_model': actual_model,
        'requested_session_id': session_id,
        'session_id': actual_session,
        'result': result,
        'raw_text': result_event.get('result'),
        'exit_code': 0,
        'observed_tool_calls': observed,
        'init_catalog': init.get('tools'),
        'tool_errors': tool_errors,
        'tool_errors_unknown': tool_errors_unknown,
        'tool_summary': _tool_summary(observed, tool_errors,
                                      tool_errors_unknown),
        'permission_scope': PERMISSION_SCOPE,
    }


def _parse_kimi(profile, stdout, session_id):
    resume_hint = None
    final_content = None
    observed = []
    tool_errors = 0
    tool_errors_unknown = 0
    for event in _events(stdout):
        role = event.get('role')
        if role == 'meta' and event.get('type') == 'session.resume_hint':
            resume_hint = event.get('session_id')
        elif role == 'assistant':
            tool_calls = event.get('tool_calls') or []
            for call in tool_calls:
                if isinstance(call, dict):
                    function = call.get('function') or {}
                    if function.get('name'):
                        observed.append(function['name'])
            content = event.get('content')
            if content is not None and not tool_calls:
                final_content = content
        elif role == 'tool':
            if 'is_error' in event:
                if event.get('is_error'):
                    tool_errors += 1
            else:
                tool_errors_unknown += 1
    if not isinstance(resume_hint, str) or not resume_hint:
        raise ValueError('resume_hint missing')
    if not isinstance(final_content, str) or not final_content:
        raise ValueError('no assistant content without tool_calls')
    result = _result_object(final_content)
    _check_tools(profile, observed)
    return {
        'adapter': 'kimi',
        'requested_model': profile.get('model'),
        'actual_model': None,
        'requested_session_id': session_id,
        'session_id': resume_hint,
        'result': result,
        'raw_text': final_content,
        'exit_code': 0,
        'observed_tool_calls': observed,
        'init_catalog': None,
        'tool_errors': tool_errors,
        'tool_errors_unknown': tool_errors_unknown,
        'tool_summary': _tool_summary(observed, tool_errors,
                                      tool_errors_unknown),
        'permission_scope': PERMISSION_SCOPE,
    }


def _result_object(raw):
    if not isinstance(raw, str):
        raise ValueError('result is not a json string')
    try:
        value = json.loads(raw)
    except ValueError as exc:
        raise ValueError('result is not valid json') from exc
    if not isinstance(value, dict):
        raise ValueError('result is not a json object')
    return value
