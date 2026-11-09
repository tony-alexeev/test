import http.client
import json
import os
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from server import Handler


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def get(self, path):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def test_health_and_version(self):
        self.assertEqual(self.get("/healthz"), (200, {"status": "ok"}))
        with patch.dict(os.environ, {"APP_VERSION": "abc123"}):
            self.assertEqual(self.get("/version"), (200, {"sha": "abc123"}))

    def test_access_uses_existing_rule(self):
        self.assertEqual(
            self.get("/access?owner_id=alice&requester_id=alice"),
            (200, {"allowed": True}),
        )
        self.assertEqual(
            self.get("/access?owner_id=alice&requester_id=bob"),
            (403, {"allowed": False}),
        )
        self.assertEqual(
            self.get("/access?owner_id=alice"),
            (403, {"allowed": False}),
        )
        self.assertEqual(
            self.get("/access?requester_id=alice"),
            (400, {"error": "owner_id is required"}),
        )

    def test_repeated_owner_is_rejected(self):
        self.assertEqual(
            self.get("/access?owner_id=alice&owner_id=bob&requester_id=alice"),
            (400, {"error": "identity parameter must appear once"}),
        )
        self.assertEqual(
            self.get("/access?owner_id=alice&requester_id=alice&requester_id=bob"),
            (400, {"error": "identity parameter must appear once"}),
        )


if __name__ == "__main__":
    unittest.main()
