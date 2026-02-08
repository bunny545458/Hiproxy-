import requests
from urllib.parse import urlparse, parse_qs

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

def handler(request):
    # OPTIONS (CORS preflight)
    if request.method == "OPTIONS":
        return ("", 200, CORS_HEADERS)

    # Read ?url=
    query = parse_qs(urlparse(request.url).query)
    target_url = query.get("url", [None])[0]

    if not target_url:
        return ("Missing ?url parameter", 400, CORS_HEADERS)

    try:
        resp = requests.get(
            target_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
            },
            timeout=10,
            allow_redirects=True
        )

        headers = CORS_HEADERS.copy()
        headers["Content-Type"] = resp.headers.get(
            "Content-Type", "text/plain"
        )

        return (resp.text, resp.status_code, headers)

    except Exception as e:
        return (f"Error: {str(e)}", 500, CORS_HEADERS)
