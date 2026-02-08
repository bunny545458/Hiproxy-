import requests
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

# =========================
# VERCEL HANDLER
# =========================
def handler(request):
    if request.method == "OPTIONS":
        return ("", 200, CORS_HEADERS)

    query = parse_qs(urlparse(request.url).query)
    target_url = query.get("url", [None])[0]

    if not target_url:
        return ("Missing ?url parameter", 400, CORS_HEADERS)

    try:
        r = requests.get(
            target_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        headers = CORS_HEADERS.copy()
        headers["Content-Type"] = r.headers.get("Content-Type", "text/plain")

        return (r.text, r.status_code, headers)

    except Exception as e:
        return (str(e), 500, CORS_HEADERS)

# =========================
# TERMUX LOCAL SERVER
# =========================
class LocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        target_url = query.get("url", [None])[0]

        self.send_response(200)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()

        if not target_url:
            self.wfile.write(b"Use: http://127.0.0.1:8000/?url=https://example.com")
            return

        try:
            r = requests.get(target_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            self.wfile.write(r.content)
        except Exception as e:
            self.wfile.write(str(e).encode())