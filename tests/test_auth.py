import unittest
from app import create_app
from app.models import db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app, _ = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_register(self):
        response = self.client.post('/auth/register', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()