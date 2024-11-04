import unittest
from app import create_app, db
from app.models import Incident, Company, Users, IncidentLog

class IncidentLogServiceTestCase(unittest.TestCase):
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

        # Crear un incidente para asociar con logs en pruebas
        response_logInc = self.client.post('/api/incident', json={
            'description': 'TestDescription',
            'source': 'web'
        }, headers={'Authorization': f'Bearer {self.user_token}'})

        response_logInc_data = response_logInc.get_json()
        self.incident_id = response_logInc_data.get('incident')
    
    def tearDown(self):
        #Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_log_successful(self):
        data = {
            'details': 'TestDescription'
        }
        response = self.client.post(f'/api/incident/{self.incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('log created', response_data['message'])

    def test_create_log_missing_fields(self):
        data = {
            # Falta el campo details
        }
        response = self.client.post(f'/api/incident/{self.incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('detail is required', response_data['message'])

    def test_get_logs(self):
        #Prueba de obtención de logs.
        response = self.client.get(f'/api/incident/{self.incident_id}/logs', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)

    def test_get_log(self):
        #Crear un log para obtener en pruebas
        data = {
            'details': 'TestDescription'
        }
        response = self.client.post(f'/api/incident/{self.incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()
        log_id = response_data.get('log')

        response = self.client.get(f'/api/incident/{self.incident_id}/logs/{log_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['details'], 'TestDescription')
    
    def test_get_log_not_found(self):
        #Prueba de log no encontrado.
        response = self.client.get(f'/api/incident/{self.incident_id}/logs/XXXX', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('log not found', response_data['message'])

    def test_get_log_not_found_incident(self):
        #Prueba de incidente no encontrado.
        response = self.client.get(f'/api/incident/XXXX/logs/XXXX', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])

    def test_update_log_successful(self):
        #Crear un log para actualizar en pruebas
        data = {
            'details': 'TestDescription'
        }
        response = self.client.post(f'/api/incident/{self.incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()
        log_id = response_data.get('log')

        data = {
            'details': 'TestDescriptionUpdated'
        }
        response = self.client.put(f'/api/incident/{self.incident_id}/logs/{log_id}', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('log updated', response_data['message'])

    def test_update_log_not_found(self):
        #Prueba de log no encontrado.
        data = {
            'details': 'TestDescription'
        }
        response = self.client.put(f'/api/incident/{self.incident_id}/logs/XXXX', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('log not found', response_data['message'])

    def test_delete_log_successful(self):
        #Crear un log para eliminar en pruebas
        data = {
            'details': 'TestDescription'
        }
        response = self.client.post(f'/api/incident/{self.incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()
        log_id = response_data.get('log')

        response = self.client.delete(f'/api/incident/{self.incident_id}/logs/{log_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('log deleted', response_data['message'])
    
    def test_delete_log_not_found(self):
        #Prueba de log no encontrado.
        response = self.client.delete(f'/api/incident/{self.incident_id}/logs/XXXX', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('log not found', response_data['message'])

if __name__ == '__main__':
    unittest.main()

