import unittest
import json
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_json(self):
        client = self.app.test_client()
        response = client.get("/json").data
        res_dict = json.loads(response)
        self.assertIn('name', res_dict, "wrong data")
        self.assertEqual(res_dict['name'], "sstranger")

    def tearDown(self):
        pass


