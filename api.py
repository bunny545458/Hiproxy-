from flask import Flask, request, Response
import requests

app = Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

@app.route("/", methods=["GET", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        return Response("", headers=CORS_HEADERS)

    target_url = request.args.get("url")
    if not target_url:
        return Response("Missing ?url parameter", status=400, headers=CORS_HEADERS)

    try:
        r = requests.get(
            target_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
            allow_redirects=True
        )

        headers = dict(CORS_HEADERS)
        headers["Content-Type"] = r.headers.get("Content-Type", "text/plain")

        return Response(r.content, status=r.status_code, headers=headers)

    except Exception as e:
        return Response(str(e), status=500, headers=CORS_HEADERS)
