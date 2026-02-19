from flask import Flask, request, Response
import requests

app = Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        return Response("", headers=CORS_HEADERS)

    target_url = request.args.get("url")
    if not target_url:
        return Response("Missing ?url parameter", status=400, headers=CORS_HEADERS)

    try:
        # ✅ Support both GET and POST
        if request.method == "POST":
            # Forward POST request with body
            r = requests.post(
                target_url,
                data=request.get_data(),
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": request.headers.get("Content-Type", "application/x-www-form-urlencoded")
                },
                timeout=30,
                allow_redirects=True
            )
        else:
            # GET request
            r = requests.get(
                target_url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30,
                allow_redirects=True
            )

        headers = dict(CORS_HEADERS)
        headers["Content-Type"] = r.headers.get("Content-Type", "text/plain")

        return Response(r.content, status=r.status_code, headers=headers)

    except Exception as e:
        return Response(str(e), status=500, headers=CORS_HEADERS)