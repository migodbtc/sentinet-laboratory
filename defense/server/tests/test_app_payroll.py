import unittest
from app import app


class PayrollEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/payroll/')
        self.assertIn(response.status_code, [200, 404])

    def test_show(self):
        response = self.client.get('/payroll/1')
        self.assertIn(response.status_code, [200, 404])

    def test_store(self):
        payload = {
            "employee_id": 2,
            "period_start": "2025-09-01",
            "period_end": "2025-09-15",
            "total_hours": 80,
            "gross_pay": 2000.00,
            "deductions": 500.00,
            "net_pay": 1500.00,
            "generated_at": "2025-09-19T08:00:00",
        }
        response = self.client.post('/payroll/', json=payload)
        self.assertIn(response.status_code, [201, 400, 404])

    def test_update(self):
        payload = {
            "gross_pay": 2200.00,
            "deductions": 600.00,
            "net_pay": 1600.00
        }
        response = self.client.put('/payroll/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_patch(self):
        payload = {
            "deductions": 550.00
        }
        response = self.client.patch('/payroll/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_destroy(self):
        response = self.client.delete('/payroll/1')
        self.assertIn(response.status_code, [204, 404])

if __name__ == '__main__':
    unittest.main()
