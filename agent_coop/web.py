"""本机只读状态页；生命周期操作目前由 CLI 提供。"""
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Coop · 隔离样例</title>
<style>
body{font:16px/1.6 system-ui;margin:3rem auto;max-width:960px;padding:0 24px;
background:#111827;color:#e5e7eb}h1{font-size:32px}small{color:#9ca3af}
section{background:#1f2937;border-radius:12px;padding:24px;margin:20px 0}
li{padding:6px}button{padding:8px 18px;cursor:pointer}pre{white-space:pre-wrap}
</style><h1>Agent Coop</h1><small>隔离协作样例 · SQLite 权威状态 · 只读</small>
<section><h2 id="phase">读取中…</h2><p id="meta"></p><p id="mode"></p>
<ol id="steps"></ol><pre id="error"></pre><button onclick="refresh()">刷新状态</button></section>
<p>启动、暂停与续作使用 CLI。暂停阻止下一步派发，在途动作完成后生效。</p>
<p>备份仅本机副本 local_only；本页不代表已合入或发布。无 OS 定时任务。</p>
<script>
async function refresh(){const phase=document.querySelector('#phase');
const meta=document.querySelector('#meta');const mode=document.querySelector('#mode');
const list=document.querySelector('#steps');const error=document.querySelector('#error');
try{const response=await fetch('/api/status',{cache:'no-store'});
if(!response.ok){let detail='状态读取失败 ('+response.status+')';
try{const body=await response.json();detail=body.error+': '+(body.detail||'');}catch(_){}
throw new Error(detail);}
const state=await response.json();
phase.textContent=state.phase+(state.paused?' · 暂停请求已保存':'');
meta.textContent='revision '+state.revision+' · 模型调用 '+state.calls_used;
const cfg=state.config||{};const m=typeof cfg.mode==='string'?cfg.mode:'';
mode.textContent='mode：'+(m||'unknown');
error.textContent=state.error||'';
list.replaceChildren();
for(const step of state.steps){const item=document.createElement('li');
item.textContent=step.name+' — '+step.status;list.appendChild(item);}
}catch(err){phase.textContent='unavailable';meta.textContent='stale';
mode.textContent='mode：unknown';list.replaceChildren();error.textContent=String(err);}}
refresh();setInterval(refresh,5000);
</script></html>'''


def error_response(handler, status, detail):
    body = json.dumps({'error': 'unavailable', 'detail': str(detail)},
                      ensure_ascii=False).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.send_header('Cache-Control', 'no-store')
    handler.end_headers()
    handler.wfile.write(body)


def make_server(root, port):
    from .store import Store

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                body, kind = PAGE.encode('utf-8'), 'text/html; charset=utf-8'
            elif self.path == '/api/status':
                try:
                    state = Store(root).read()
                except (RuntimeError, ValueError, OSError, sqlite3.Error) as error:
                    error_response(self, 503, error)
                    return
                body = json.dumps(state, ensure_ascii=False).encode('utf-8')
                kind = 'application/json; charset=utf-8'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def serve(root, port):
    with make_server(root, port) as server:
        print(f'http://127.0.0.1:{server.server_port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
