"""CodeBuddy / Kimi 命令构造与 stream-json 协议解析。"""
import json

PERMISSION_SCOPE = 'cli_tool_filter_not_os_sandbox'


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
    tools_arg = ','.join(tools)
    argv = [
        profile['executable'],
        profile['entry'],
        '-p', prompt,
        '--model', profile['model'],
        '--session-id', session_id,
        '--tools', tools_arg,
        '--allowedTools', tools_arg,
        '--strict-mcp-config',
        '--mcp-config', '{"mcpServers":{}}',
        '--max-turns', str(max_turns),
        '--output-format', 'stream-json',
        '--verbose',
    ]
    if 'Write' in tools or 'Edit' in tools:
        argv += ['--permission-mode', 'acceptEdits']
    return argv


def _kimi_command(profile, prompt):
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
