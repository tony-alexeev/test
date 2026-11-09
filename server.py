"""Synthetic HTTP fixture for the report access rule."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from access import can_view_report


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/healthz":
            self.respond(200, {"status": "ok"})
            return
        if url.path == "/version":
            self.respond(200, {"sha": os.environ.get("APP_VERSION", "dev")})
            return
        if url.path == "/access":
            query = parse_qs(url.query, keep_blank_values=True)
            if len(query.get("owner_id", [])) > 1 or len(query.get("requester_id", [])) > 1:
                self.respond(400, {"error": "identity parameter must appear once"})
                return
            owner = query.get("owner_id", [""])[0]
            requester = query.get("requester_id", [None])[0]
            if not owner:
                self.respond(400, {"error": "owner_id is required"})
                return
            allowed = can_view_report(owner, requester)
            self.respond(200 if allowed else 403, {"allowed": allowed})
            return
        self.respond(404, {"error": "not found"})

    def respond(self, status, body):
        data = json.dumps(body, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
