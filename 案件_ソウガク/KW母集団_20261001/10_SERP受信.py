# -*- coding: utf-8 -*-
"""ブラウザで抽出したGoogle検索結果（JSON）を受け取ってファイルに保存するだけの受け口。

アプリ内ブラウザの google.co.jp ページから fetch で送られたJSONを
serp/round{n}/{連番}.json に書き出す。127.0.0.1 だけで待ち受け、外部には公開しない。
起動: python 10_SERP受信.py
"""
from __future__ import annotations

import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORT = 8765


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        """/save#<JSON> を開くと、このページ自身が #以降のJSONを POST して保存する。
        google.co.jp のページからは CSP で直接送れないため、タブをここへ移動させて受け取る。"""
        page = """<!doctype html><meta charset="utf-8"><title>SERP保存</title><pre id="r">saving...</pre>
<script>
const raw = decodeURIComponent(location.hash.slice(1));
fetch('/', {method:'POST', headers:{'Content-Type':'application/json'}, body: raw})
  .then(r => r.json()).then(j => { document.getElementById('r').textContent = JSON.stringify(j); document.title = 'SAVED ' + (j.file || 'NG'); })
  .catch(e => { document.getElementById('r').textContent = 'ERROR ' + e; document.title = 'ERROR'; });
</script>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            data = json.loads(body.decode("utf-8"))
            rnd = int(data.get("round", 0))
            out = HERE / "serp" / f"round{rnd}"
            out.mkdir(parents=True, exist_ok=True)
            n = len(list(out.glob("*.json"))) + 1
            data["saved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            (out / f"{n:03d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            msg = {"ok": True, "file": f"round{rnd}/{n:03d}.json"}
            print(f"saved round{rnd}/{n:03d} q={data.get('q')}", flush=True)
        except Exception as exc:  # 受け取れなかった場合はそのまま返す
            msg = {"ok": False, "error": str(exc)}
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(msg).encode("utf-8"))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"listening 127.0.0.1:{PORT}", flush=True)
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
