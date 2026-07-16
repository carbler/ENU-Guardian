#!/usr/bin/env python3
"""Local dev server: serves the static app and implements /api/draft
reading DEEP_SEEK_API_KEY from .env — same contract as the Vercel function.

Usage: python3 dev-server.py [port]
"""
import json
import os
import ssl
import sys
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # macOS system Python often lacks CA certs; certifi fixes it
    SSL_CONTEXT = ssl.create_default_context()


def load_env_key():
    key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("DEEP_SEEK_API_KEY")
    if key:
        return key
    env_path = os.path.join(ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith(("DEEP_SEEK_API_KEY=", "DEEPSEEK_API_KEY=")):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


API_KEY = load_env_key()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.rstrip("/") == "/api/draft":
            return self.send_json(200, {"configured": bool(API_KEY)})
        return super().do_GET()

    def do_POST(self):
        if self.path.rstrip("/") != "/api/draft":
            return self.send_json(404, {"error": "not found"})
        if not API_KEY:
            return self.send_json(503, {"error": "DEEP_SEEK_API_KEY not configured"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            system, user = payload.get("system"), payload.get("user")
            if not isinstance(system, str) or not isinstance(user, str):
                return self.send_json(400, {"error": "invalid payload"})
            req = urllib.request.Request(
                "https://api.deepseek.com/chat/completions",
                data=json.dumps({
                    "model": "deepseek-chat",
                    "temperature": 0.7,
                    "max_tokens": 300,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                }).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}",
                },
            )
            with urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT) as resp:
                data = json.loads(resp.read())
            text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
            if not text:
                return self.send_json(502, {"error": "empty completion"})
            return self.send_json(200, {"text": text})
        except urllib.error.HTTPError as e:
            detail = f"HTTP {e.code}"
            try:
                detail = json.loads(e.read()).get("error", {}).get("message", detail)
            except Exception:
                pass
            return self.send_json(502, {"error": detail})
        except Exception as e:
            return self.send_json(502, {"error": str(e)})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"ENU Guardian dev server → http://localhost:{port}")
    print(f"DeepSeek key: {'configured' if API_KEY else 'NOT FOUND (add DEEP_SEEK_API_KEY to .env)'}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
