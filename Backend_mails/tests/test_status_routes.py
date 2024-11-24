import unittest
from app import create_app, db

class StatusServiceTestCases(unittest.TestCase):
    def setUp(self):
        #Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()


    def tearDown(self):
        #Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_status_successful(self):
        response = self.client.get('/')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Backend Emails running', response_data['message'])