import unittest
from app import create_app, db
from app.models.models import Users, Company

class UsersServiceTestCase(unittest.TestCase):
    def setUp(self):
        #Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crear una empresa para asociar con usuarios en pruebas
        self.company = Company(name="TestCompany")
        db.session.add(self.company)
        db.session.commit()

    def tearDown(self):
        #Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_successful(self):
        #Prueba de registro de usuario exitoso.
        data = {
            'username': 'testuser',
            'password': 'Test@1234',
            'role': 'customer',
            'company_id': self.company.id,
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/api/register', json=data)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('users created successfully', response_data['message'])

    def test_register_missing_fields(self):
        #Prueba de error por campos faltantes en registro.
        data = {
            'username': 'testuser',
            'password': 'Test@1234'
            # Falta el resto de los campos
        }
        response = self.client.post('/api/register', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('role is required', response_data['message'])

    def test_register_invalid_email(self):
        #Prueba de error por email inválido en registro.
        data = {
            'username': 'testuser',
            'password': 'Test@1234',
            'role': 'customer',
            'company_id': self.company.id,
            'email': 'invalid-email',
            'phone': '1234567890',
            'name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/api/register', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email', response_data['message'])

    def test_login_success(self):
        #Prueba de autenticación exitosa.
        # Primero registrar un usuario
        data = {
            'username': 'testuser',
            'password': 'Test@1234',
            'role': 'customer',
            'company_id': self.company.id,
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'last_name': 'User'
        }
        self.client.post('/api/register', json=data)
        
        # Ahora probar login
        login_data = {'username': 'testuser', 'password': 'Test@1234'}
        response = self.client.post('/api/login', json=login_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response_data)

    def test_login_invalid_credentials(self):
        #Prueba de error por credenciales inválidas en login.
        login_data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post('/api/login', json=login_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response_data['message'])

    def test_update_user_successful(self):
        #Prueba de actualización exitosa del usuario.
        # Crear usuario
        data = {
            'username': 'testuser',
            'password': 'Test@1234',
            'role': 'customer',
            'company_id': self.company.id,
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'last_name': 'User'
        }
        response_register = self.client.post('/api/register', json=data)
        response_register_data = response_register.get_json()

        login_data = {'username': 'testuser', 'password': 'Test@1234'}
        response_login = self.client.post('/api/login', json=login_data)
        response_login_data = response_login.get_json()

        user_id = response_register_data.get('id')

        # Actualizar usuario
        update_data = {'phone': '0987654321'}
        response = self.client.put(f'/api/user/{user_id}', json=update_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('users updated successfully', response_data['message'])

    def test_delete_user_successful(self):
         #Prueba de eliminación exitosa de un usuario.
         # Crear un usuario
         data = {
             'username': 'testuser',
             'password': 'Test@1234',
             'role': 'customer',
             'company_id': self.company.id,
             'email': 'testuser@example.com',
             'phone': '1234567890',
             'name': 'Test',
             'last_name': 'User'
         }

         self.client.post('/api/register', json=data)

         login_data = {'username': 'testuser', 'password': 'Test@1234'}
         response_login = self.client.post('/api/login', json=login_data)
         response_login_data = response_login.get_json()

         user_token = response_login_data.get('access_token')

         response_get_user = self.client.get('/api/user', headers={'Authorization': f'Bearer {user_token}'})
         response_get_user_data=response_get_user.get_json()
         user_id = response_get_user_data.get('id')

         # Eliminar usuario
         delete_response = self.client.delete(f'/api/user/{user_id}')
         delete_response_data = delete_response.get_json()
         self.assertEqual(delete_response.status_code, 200)
         self.assertIn('users deleted successfully', delete_response_data['message'])

if __name__ == '__main__':
    unittest.main()
