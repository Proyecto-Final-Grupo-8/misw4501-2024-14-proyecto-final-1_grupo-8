import unittest
from app import create_app, db
from app.models import Incident, Company, Users

class IncidentServiceTestCase(unittest.TestCase):
    def setUp(self):
        #Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Crear una empresa para asociar con incidentes en pruebas
        self.company = Company(name="TestCompany")
        db.session.add(self.company)
        db.session.commit()

        # Crear un usuario para asociar con incidentes en pruebas
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
        
        # Login para obtener token
        login_data = {'username': 'testuser', 'password': 'Test@1234'}
        response_login = self.client.post('/api/login', json=login_data)
        response_login_data = response_login.get_json()
        self.user_token = response_login_data.get('access_token')

        
    def tearDown(self):
        #Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_incident_successful(self):
        data = {
            'description': 'TestDescription',
            'source': 'web'
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('incident created', response_data['message'])
    
    def test_create_incident_missing_fields(self):
        data = {
            # Falta el campo description
            'source': 'web'
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('description is required', response_data['message'])

    def test_create_incident_invalid_source(self):
        data = {
            'description': 'TestDescription',
            'source': 'invalid-source'
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('source is invalid', response_data['message'])

    def test_get_incidents(self):
        response = self.client.get('/api/incidents', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)

    def test_get_incident(self):
        data={
            'description': 'TestDescription',
            'source': 'web'
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()
        


if __name__ == '__main__':
    unittest.main()