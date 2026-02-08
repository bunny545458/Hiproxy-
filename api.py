import requests
from urllib.parse import urlparse, parse_qs

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

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
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
            },
            timeout=10,
            allow_redirects=True
        )

        headers = CORS_HEADERS.copy()
        headers["Content-Type"] = r.headers.get(
            "Content-Type", "text/plain"
        )

        return (r.text, r.status_code, headers)

    except Exception as e:
        return (str(e), 500, CORS_HEADERS)
