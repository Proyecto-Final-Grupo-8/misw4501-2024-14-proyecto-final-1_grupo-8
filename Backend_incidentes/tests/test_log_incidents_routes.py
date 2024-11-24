import unittest
from app import create_app, db
from app.models import Incident, Company, Users, IncidentLog
from unittest.mock import patch
from flask_jwt_extended import create_access_token

class IncidentLogServiceTestCase(unittest.TestCase):
    def setUp(self):
        # Configura el entorno de prueba antes de cada test
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

        # Crear un usuario ficticio en la base de datos
        self.user = Users(
            username="testuser",
            role="customer",
            company_id=self.company.id,
            email="testuser@example.com",
            phone="1234567890",
            name="Test",
            last_name="User",
            password_hash="fake_hashed_password"  # Simula un hash
        )
        db.session.add(self.user)
        db.session.commit()

        # Generar un token JWT directamente
        self.user_token = create_access_token(identity=self.user.id)

        # Mock para evitar dependencia de login
        patch('flask_jwt_extended.get_jwt_identity', return_value=self.user.id).start()

        # Crear un incidente para asociar con logs en pruebas
        response_logInc = self.client.post('/api/incident', json={
            'description': 'TestDescription',
            'source': 'web'
        }, headers={'Authorization': f'Bearer {self.user_token}'})

        response_logInc_data = response_logInc.get_json()
        self.incident_id = response_logInc_data.get('incident')

    def tearDown(self):
        # Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        patch.stopall()


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

    def test_create_incident_invalid_source(self):
        data = {
            'description': 'Test description',
            'source': 'invalid_source'  # Valor no permitido
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('source is invalid', response_data['message'])

    def test_create_incident_missing_description(self):
        data = {
            'source': 'web'
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('description is required', response_data['message'])
 
    def test_create_log_nonexistent_incident(self):
        data = {
            'details': 'Test log'
        }
        response = self.client.post('/api/incident/invalid_incident_id/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])

    def test_update_incident_customer(self):
        data = {
            'status': 'Closed'
        }
        response = self.client.put(f'/api/incident/{self.incident_id}', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertIn('you are not allowed to update this incident', response_data['message'])

    def test_delete_incident_unauthorized(self):
        response = self.client.delete(f'/api/incident/{self.incident_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertIn('you are not allowed to delete this incident', response_data['message'])


    def test_create_incident_and_add_logs(self):
        # Crear un incidente
        data = {
            'description': 'Workflow test',
            'source': 'web'
        }
        response = self.client.post('/api/incident', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(response.status_code, 201)

        incident_id = response.get_json().get('incident')

        # Añadir logs al incidente
        log_data = {
            'details': 'Log entry 1'
        }
        response = self.client.post(f'/api/incident/{incident_id}/logs', json=log_data, headers={'Authorization': f'Bearer {self.user_token}'})
        self.assertEqual(response.status_code, 201)

        # Verificar los logs
        response = self.client.get(f'/api/incident/{incident_id}/logs', headers={'Authorization': f'Bearer {self.user_token}'})
        logs = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['details'], 'Log entry 1')

    def test_delete_incident_with_logs(self):
        # Crear un log asociado al incidente
        log_data = {
            'details': 'Log to delete'
        }
        self.client.post(f'/api/incident/{self.incident_id}/logs', json=log_data, headers={'Authorization': f'Bearer {self.user_token}'})

        # Intentar eliminar el incidente
        response = self.client.delete(f'/api/incident/{self.incident_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertIn('you are not allowed to delete this incident', response_data['message'])

    def test_delete_nonexistent_log(self):
        response = self.client.delete('/api/incident/invalid_incident_id/logs/invalid_log_id', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])

    def test_update_nonexistent_incident(self):
        data = {
            'description': 'Updated description'
        }
        response = self.client.put('/api/incident/invalid_id', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])

    def test_get_all_incidents_empty(self):
        Incident.query.delete()
        db.session.commit()

        response = self.client.get('/api/incidents', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, []) 


    def test_create_log_valid_incident(self):
        data = {
            'details': 'Valid log creation'
        }
        response = self.client.post(f'/api/incident/{self.incident_id}/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('log created', response_data['message'])

    def test_delete_nonexistent_incident(self):
        response = self.client.delete('/api/incident/invalid_incident_id', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])

    def test_get_nonexistent_log_in_valid_incident(self):
        response = self.client.get(f'/api/incident/{self.incident_id}/logs/invalid_log_id', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('log not found', response_data['message'])

    @patch('app.models.Incident.query.all', side_effect=Exception("Database error"))
    def test_get_all_incident_exception(self, mock_query):

        Incident.query.delete()
        db.session.commit()

        response = self.client.get('/api/incidents', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, [])

    def test_get_incident_by_id_as_analyst(self):
        self.user.role = 'analyst'
        db.session.commit()

        response = self.client.get(f'/api/incident/{self.incident_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['id'], self.incident_id)

    def test_get_incident_by_id_as_admin(self):
        self.user.role = 'admin'
        db.session.commit()

        response = self.client.get(f'/api/incident/{self.incident_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['id'], self.incident_id)

    def test_update_incident_as_analyst(self):
        self.user.role = 'analyst'
        db.session.commit()

        data = {'status': 'Progress'}
        response = self.client.put(f'/api/incident/{self.incident_id}', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('incident updated', response_data['message'])

    def test_update_incident_as_admin(self):
        self.user.role = 'admin'
        db.session.commit()

        data = {
            'description': 'Updated Description',
            'customer_id': self.user.id,
            'source': 'app',
            'status': 'Closed'
        }
        response = self.client.put(f'/api/incident/{self.incident_id}', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('incident updated', response_data['message'])

    def test_delete_nonexistent_incident(self):
        response = self.client.delete('/api/incident/nonexistent_id', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])

    def test_delete_incident_as_admin(self):
        self.user.role = 'admin'
        db.session.commit()

        response = self.client.delete(f'/api/incident/{self.incident_id}', headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('incident deleted', response_data['message'])

    def test_create_log_invalid_incident(self):
        data = {'details': 'Invalid Incident Log'}
        response = self.client.post('/api/incident/invalid_id/logs', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('incident not found', response_data['message'])


if __name__ == '__main__':
    unittest.main()

