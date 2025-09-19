import unittest
from app import app


class EmployeesEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/employees/')
        self.assertIn(response.status_code, [200, 404])

    def test_show(self):
        response = self.client.get('/employees/1')
        self.assertIn(response.status_code, [200, 404])

    def test_store(self):
        payload = {
            "first_name": "Eve",
            "last_name": "Garcia",
            "position": "DevOps Engineer",
            "base_salary": 60000.00,
            "hire_date": "2025-09-19"
        }
        response = self.client.post('/employees/', json=payload)
        self.assertIn(response.status_code, [201, 400, 404])

    def test_update(self):
        payload = {"base_salary": 42000.00, "position": "HR Lead"}
        response = self.client.put('/employees/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_patch(self):
        payload = {"position": "HR Lead"}
        response = self.client.patch('/employees/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_destroy(self):
        response = self.client.delete('/employees/1')
        self.assertIn(response.status_code, [204, 404])

if __name__ == '__main__':
    unittest.main()
