from app.models import db

class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.app, _ = create_app()
        self.client = self.app.test_client() 
        with self.app.app_context():
            db.create_all()

    def test_create_document(self):
        self.client.post('/auth/register', data={'email': 'test@example.com', 'password': 'password123'})
        self.client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password123'})
        response = self.client.post('/doc/editor/1', data={'content': 'Test content'})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()