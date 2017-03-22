from django.test import TestCase

class thothViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/student/')
        self.assertEqual(resp.status_code, 200)