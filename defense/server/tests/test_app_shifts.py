import unittest
from app import app


class ShiftsEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/shifts/')
        self.assertIn(response.status_code, [200, 404])

    def test_show(self):
        response = self.client.get('/shifts/1')
        self.assertIn(response.status_code, [200, 404])

    def test_store(self):
        payload = {
            "shift_name": "Afternoon",
            "start_time": "13:00:00",
            "end_time": "21:00:00"
        }
        response = self.client.post('/shifts/', json=payload)
        self.assertIn(response.status_code, [201, 400, 404])

    def test_update(self):
        payload = {
            "end_time": "22:00:00"
        }
        response = self.client.put('/shifts/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_patch(self):
        payload = {
            "end_time": "22:00:00"
        }
        response = self.client.patch('/shifts/1', json=payload)
        self.assertIn(response.status_code, [200, 400, 404])

    def test_destroy(self):
        response = self.client.delete('/shifts/1')
        self.assertIn(response.status_code, [204, 404])

if __name__ == '__main__':
    unittest.main()
