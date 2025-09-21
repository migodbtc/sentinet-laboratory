import unittest
from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_login(self):
        payload = {"username": "alice.santos", "password": "hashed_password_1"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())
        self.assertIn("refresh_token", response.get_json())

    def test_logout(self):
        # Simulate login to get token
        payload = {"username": "alice.santos", "password": "hashed_password_1"}
        login_response = self.client.post("/login", json=payload)
        self.assertEqual(login_response.status_code, 200)  # Ensure login is successful

        access_token = login_response.get_json()["access_token"]

        # Test logout
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.post("/logout", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "Logged out successfully")

    def test_refresh(self):
        # Simulate login to get refresh token
        payload = {"username": "alice.santos", "password": "hashed_password_1"}
        login_response = self.client.post("/login", json=payload)
        refresh_token = login_response.get_json()["refresh_token"]

        # Test refresh
        response = self.client.post("/refresh", json={"refresh_token": refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())

if __name__ == "__main__":
    unittest.main()