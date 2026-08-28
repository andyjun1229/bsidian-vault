#!/usr/bin/env python3
"""本地网页工具：粘贴链接后一键导入 raw。"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs


HTML_PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>URL -> RAW 导入工具</title>
  <style>
    :root { --bg:#f5f7fb; --card:#fff; --text:#0f172a; --muted:#475569; --line:#dbe3ef; --brand:#2563eb; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; background:linear-gradient(120deg,#eef4ff,#f8fbff); color:var(--text); }
    .wrap { max-width:860px; margin:40px auto; padding:0 16px; }
    .card { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; box-shadow:0 10px 30px rgba(15,23,42,.05); }
    h1 { font-size:22px; margin:0 0 8px; }
    p { margin:0 0 16px; color:var(--muted); }
    label { display:block; margin:14px 0 6px; font-size:14px; color:#334155; }
    input { width:100%; padding:11px 12px; border:1px solid #cfd8e6; border-radius:10px; font-size:14px; }
    input:focus { outline:none; border-color:var(--brand); box-shadow:0 0 0 3px rgba(37,99,235,.15); }
    .row { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .btns { margin-top:16px; display:flex; gap:10px; }
    button { padding:10px 14px; border:none; border-radius:10px; cursor:pointer; font-size:14px; }
    .primary { background:var(--brand); color:#fff; }
    .ghost { background:#e8efff; color:#1e40af; }
    .result { margin-top:18px; white-space:pre-wrap; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px; background:#0b1220; color:#d6e4ff; padding:14px; border-radius:10px; }
    .hint { margin-top:12px; font-size:12px; color:#64748b; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>URL -> RAW 导入工具</h1>
      <p>粘贴文章链接，点击导入，会自动写入 <code>raw/</code> 并补齐元数据。</p>
      <form method="POST" action="/import">
        <label>文章链接（必填）</label>
        <input name="url" placeholder="https://..." required />

        <div class="row">
          <div>
            <label>来源分类（可选）</label>
            <input name="category" placeholder="例如：公众号 / 网页 / 自己" />
          </div>
          <div>
            <label>发布日期（可选）</label>
            <input name="date" placeholder="YYYY-MM-DD" />
          </div>
        </div>

        <label>标题覆盖（可选）</label>
        <input name="title" placeholder="不填则自动读取网页标题" />

        <div class="btns">
          <button class="primary" type="submit" name="mode" value="write">导入到 raw</button>
          <button class="ghost" type="submit" name="mode" value="dry">预览（不落盘）</button>
        </div>
      </form>
      {result_html}
      <div class="hint">启动命令：<code>python3 scripts/url_to_raw_web.py</code>，默认地址：<code>http://127.0.0.1:8765</code></div>
    </div>
  </div>
</body>
</html>
"""


def render_page(result: str = "") -> bytes:
    result_html = ""
    if result:
        result_html = f'<div class="result">{html.escape(result)}</div>'
    return HTML_PAGE.format(result_html=result_html).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    script_path: Path
    vault_path: Path

    def _send_html(self, body: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in {"/", "/index.html"}:
            self._send_html(render_page())
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self):
        if self.path != "/import":
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length).decode("utf-8", errors="replace")
        data = parse_qs(payload)

        url = (data.get("url", [""])[0] or "").strip()
        category = (data.get("category", [""])[0] or "").strip()
        title = (data.get("title", [""])[0] or "").strip()
        date = (data.get("date", [""])[0] or "").strip()
        mode = (data.get("mode", ["write"])[0] or "write").strip()

        if not url:
            self._send_html(render_page("[ERROR] 文章链接不能为空"), status=400)
            return

        cmd = [
            sys.executable,
            str(self.script_path),
            url,
            "--vault",
            str(self.vault_path),
        ]
        if category:
            cmd.extend(["--category", category])
        if title:
            cmd.extend(["--title", title])
        if date:
            cmd.extend(["--date", date])
        if mode == "dry":
            cmd.append("--dry-run")

        try:
            cp = subprocess.run(cmd, check=False, capture_output=True, text=True)
        except Exception as exc:
            self._send_html(render_page(f"[ERROR] 执行失败: {exc}"), status=500)
            return

        out = (cp.stdout or "") + (cp.stderr or "")
        status = 200 if cp.returncode == 0 else 500
        self._send_html(render_page(out.strip() or "[INFO] 无输出"), status=status)

    def log_message(self, fmt, *args):
        return


def main() -> int:
    ap = argparse.ArgumentParser(description="URL -> RAW 本地网页导入工具")
    ap.add_argument("--host", default="127.0.0.1", help="默认 127.0.0.1")
    ap.add_argument("--port", type=int, default=8765, help="默认 8765")
    ap.add_argument("--vault", default=str(Path(__file__).resolve().parents[1]), help="Vault 根目录")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    script_path = Path(__file__).resolve().parent / "url_to_raw.py"
    if not script_path.exists():
        print(f"[ERROR] 未找到脚本: {script_path}")
        return 1

    Handler.script_path = script_path
    Handler.vault_path = vault

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[OK] URL -> RAW 网页工具已启动: http://{args.host}:{args.port}")
    print(f"[INFO] Vault: {vault}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] 已停止")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
