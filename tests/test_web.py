"""只读 Web 直接使用同一 SQLite 状态。"""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


class WebTests(unittest.TestCase):
    def test_status_tracks_pause_and_rejects_write(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        from agent_coop.web import make_server
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            store = Store(root)
            store.initialize({'mode': 'test'}, ['one'])
            server = make_server(root, 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            url = f'http://127.0.0.1:{server.server_port}/api/status'
            try:
                store.pause()
                with urllib.request.urlopen(url, timeout=3) as response:
                    status = json.load(response)
                    self.assertEqual(response.headers['Cache-Control'], 'no-store')
                self.assertEqual(status['revision'], store.read()['revision'])
                self.assertTrue(status['paused'])
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(urllib.request.Request(url, data=b'{}'), timeout=3)
                self.assertEqual(error.exception.code, 501)
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=3)

    def test_status_exposes_config_mode(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        from agent_coop.web import make_server
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            Store(root).initialize({'mode': 'test'}, ['one'])
            server = make_server(root, 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            url = f'http://127.0.0.1:{server.server_port}/api/status'
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    status = json.load(response)
                self.assertEqual(status['config']['mode'], 'test')
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=3)

    def test_status_tracks_revision_across_updates(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        from agent_coop.web import make_server
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            Store(root).initialize({'mode': 'test'}, ['one'])
            server = make_server(root, 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            url = f'http://127.0.0.1:{server.server_port}/api/status'
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    first = json.load(response)
                Store(root).pause()
                with urllib.request.urlopen(url, timeout=3) as response:
                    second = json.load(response)
                self.assertGreater(second['revision'], first['revision'])
                self.assertEqual(second['revision'], Store(root).read()['revision'])
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=3)

    def test_read_failure_returns_error_and_no_cache(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        from agent_coop.web import make_server
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            store = Store(root)
            store.initialize({'mode': 'test'}, ['one'])
            server = make_server(root, 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            url = f'http://127.0.0.1:{server.server_port}/api/status'
            try:
                (root / '.runtime' / 'state.sqlite').write_bytes(b'not a sqlite database')
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(url, timeout=3)
                self.assertGreaterEqual(error.exception.code, 400)
                self.assertEqual(error.exception.headers['Cache-Control'], 'no-store')
                self.assertIn(b'unavailable', error.exception.read())
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=3)

    def test_page_marks_mode_local_only_and_unavailable(self):
        from agent_coop.paths import create_root
        from agent_coop.store import Store
        from agent_coop.web import make_server
        with tempfile.TemporaryDirectory() as directory:
            root = create_root(Path(directory) / 'sample')
            Store(root).initialize({'mode': 'test'}, ['one'])
            server = make_server(root, 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                with urllib.request.urlopen(
                        f'http://127.0.0.1:{server.server_port}/', timeout=3) as response:
                    self.assertEqual(response.headers['Cache-Control'], 'no-store')
                    html = response.read().decode('utf-8')
                for marker in ('local_only', 'mode', 'unknown', 'unavailable'):
                    self.assertIn(marker, html)
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=3)
