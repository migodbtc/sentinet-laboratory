import unittest
from app import app

class RegisterRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_register_success(self):
        payload = {"username": "new.user", "password": "secure_password"}
        response = self.client.post("/register", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "User registered successfully")

    def test_register_missing_fields(self):
        payload = {"username": "incomplete.user"}
        response = self.client.post("/register", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Username and password are required")

    def test_register_duplicate_user(self):
        payload = {"username": "alice.santos", "password": "password"}
        response = self.client.post("/register", json=payload)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json()["message"], "Username already exists")

if __name__ == "__main__":
    unittest.main()