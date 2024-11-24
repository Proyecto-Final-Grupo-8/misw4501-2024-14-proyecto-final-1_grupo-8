import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Company

class IncidentLogServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Crear una empresa para pruebas
        self.company = Company(name="TestCompany")
        db.session.add(self.company)
        db.session.commit()

        # Registrar un usuario y obtener un token
        self.client.post('/api/register', json={
            'username': 'testuser',
            'password': 'Test@1234',
            'role': 'customer',
            'company_id': self.company.id,
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'last_name': 'User'
        })

        login_data = {'username': 'testuser', 'password': 'Test@1234'}
        response_login = self.client.post('/api/login', json=login_data)
        response_login_data = response_login.get_json()
        self.user_token = response_login_data.get('access_token')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.routes.incident_routes.requests.post')
    def test_create_log_successful(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"message": "log created"}

        incident_id = "1"
        data = {'details': 'TestDescription'}
        response = self.client.post(f'/api/incident/{incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["message"], "log created")

    @patch('app.routes.incident_routes.requests.get')
    def test_get_logs(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "details": "LogDetail"}]

        incident_id = "1"
        response = self.client.get(f'/api/incident/{incident_id}/logs', headers={'Authorization': f'Bearer {self.user_token}'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

if __name__ == '__main__':
    unittest.main()