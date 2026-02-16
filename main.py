from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Minimal JSON API built on the Python standard library."""

    server_version = "SimplePythonAPI/0.1"

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_not_found(self) -> None:
        self._send_json({"error": "Not found"}, status=404)

    def _send_method_not_allowed(self) -> None:
        self._send_json({"error": "Method not allowed"}, status=405)

    def _send_bad_request(self, message: str) -> None:
        self._send_json({"error": message}, status=400)

    def _json_body(self) -> Dict[str, Any] | None:
        length = self.headers.get("Content-Length")
        if not length:
            return None

        try:
            size = int(length)
        except ValueError:
            self._send_bad_request("Invalid Content-Length")
            return None

        if size <= 0:
            return None

        raw = self.rfile.read(size)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "Body is not valid JSON"}, status=400)
            return None

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json({"status": "ok", "service": "simple-api"})
            return

        if path == "/api/hello":
            query = parse_qs(parsed.query)
            name = query.get("name", ["world"])[0]
            self._send_json({"message": f"Hello, {name}!"})
            return

        if path == "/":
            self._send_json({"message": "Simple API is running. Try /health or /api/hello?name=you."})
            return

        self._send_not_found()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path != "/api/echo":
            self._send_not_found()
            return

        payload = self._json_body()
        if payload is None:
            return

        self._send_json({
            "message": "payload received",
            "received": payload,
        })


def run() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    server = HTTPServer((host, port), SimpleAPIHandler)
    print(f"Starting API on http://{host}:{port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
