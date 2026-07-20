import unittest

from app import fetch_user, mask_token, process_payload, require_role, sanitize_input, verify_password


class TestSecureApp(unittest.TestCase):
    def test_sanitize_input(self):
        self.assertEqual(sanitize_input("  hello  "), "hello")

    def test_verify_password(self):
        digest = __import__("hashlib").sha256(b"secret").hexdigest()
        self.assertTrue(verify_password(digest, "secret"))
        self.assertFalse(verify_password(digest, "wrong"))

    def test_require_role(self):
        self.assertTrue(require_role({"authenticated": True, "role": "admin"}, "admin"))
        self.assertFalse(require_role({"authenticated": True, "role": "user"}, "admin"))

    def test_process_payload(self):
        self.assertEqual(process_payload({"name": "alice"}), {"name": "alice", "status": "ok"})

    def test_mask_token(self):
        self.assertEqual(mask_token("abcd"), "****")

    def test_fetch_user(self):
        class Cursor:
            def execute(self, _query, _params):
                return None

            def fetchone(self):
                return {"id": "1", "name": "alice"}

        self.assertEqual(fetch_user("1", Cursor()), {"id": "1", "name": "alice"})


if __name__ == "__main__":
    unittest.main()
