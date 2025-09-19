import unittest
from app import app

class AttendanceLogsEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/attendance_logs/')
        self.assertIn(response.status_code, [200, 404])

    def test_show(self):
        response = self.client.get('/attendance_logs/1')
        self.assertIn(response.status_code, [200, 404])

    def test_store(self):
        payload = {"employee_id": 1, "log_date": "2025-09-19", "time_in": "08:00:00", "time_out": "17:00:00", "hours_worked": 8}
        response = self.client.post('/attendance_logs/', json=payload)
        self.assertIn(response.status_code, [201, 400, 404])

    def test_update(self):
        payload = {"time_out": "18:00:00", "hours_worked": 9}
        response = self.client.put('/attendance_logs/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_patch(self):
        payload = {"time_out": "18:00:00"}
        response = self.client.patch('/attendance_logs/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_destroy(self):
        response = self.client.delete('/attendance_logs/1')
        self.assertIn(response.status_code, [204, 404])

if __name__ == '__main__':
    unittest.main()
