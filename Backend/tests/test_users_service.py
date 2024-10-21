# tests/test_users_service.py

from datetime import datetime
import unittest
from app import create_app, db
from app.models.models import Users, Company, Contract
from app.services.users_service import create_users, authenticate_users, get_users_info, create_contrac_and_company

class UsersServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Configurar el entorno de prueba antes de cada test."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crear un contrato para pruebas con fechas como objetos datetime.date
        self.contrac = Contract(
            description="Test Contract", 
            start_date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2025-01-01', '%Y-%m-%d').date()
        )
        db.session.add(self.contrac)
        db.session.commit()

        # Crear una empresa para pruebas con contrac_id asociado
        self.company = Company(name="TestCompany", contrac_id=self.contrac.id)
        db.session.add(self.company)
        db.session.commit()

        # Crear un usuario para pruebas
        self.user = Users(username="testuser", role="admin", company=self.company)
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Limpiar después de cada prueba."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_users_success(self):
        """Prueba de éxito para la creación de usuarios."""
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'role': 'customer',
            'company_id': self.company.id
        }

        response, status_code = create_users(data)
        self.assertEqual(status_code, 201)
        self.assertEqual(response['message'], 'users created successfully')

        user = Users.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.role, 'customer')

    def test_create_users_existing_user(self):
        """Prueba para cuando ya existe el usuario."""
        data = {
            'username': 'testuser',
            'password': 'password',
            'role': 'admin',
            'company_id': self.company.id
        }

        response, status_code = create_users(data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], 'users already exists')

    def test_create_users_invalid_role(self):
        """Prueba para un rol inválido."""
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'role': 'invalidrole',
            'company_id': self.company.id
        }

        response, status_code = create_users(data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], 'Invalid role specified')

    def test_authenticate_users_success(self):
        """Prueba de éxito para la autenticación de usuarios."""
        data = {
            'username': 'testuser',
            'password': 'password'
        }

        response, status_code = authenticate_users(data)
        self.assertEqual(status_code, 200)
        self.assertIn('access_token', response)

    def test_authenticate_users_invalid_credentials(self):
        """Prueba para credenciales inválidas."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response, status_code = authenticate_users(data)
        self.assertEqual(status_code, 401)
        self.assertEqual(response['message'], 'Invalid credentials')

    def test_get_users_info_success(self):
        """Prueba para obtener la información de un usuario con éxito."""
        response, status_code = get_users_info(self.user.id)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['username'], 'testuser')
        self.assertEqual(response['role'], 'admin')
        self.assertEqual(response['company'], 'TestCompany')

    def test_get_users_info_not_found(self):
        """Prueba para cuando el usuario no existe."""
        response, status_code = get_users_info(999)
        self.assertEqual(status_code, 404)
        self.assertEqual(response['message'], 'users not found')

    def test_create_contrac_and_company_success(self):
        """Prueba de éxito para la creación de contrato y empresa."""
        data = {
            'description': 'Test Contract',
            'start_date': '2024-01-01',
            'end_date': '2025-01-01',
            'name_company': 'NewCompany'
        }

        response, status_code = create_contrac_and_company(data)
        self.assertEqual(status_code, 201)
        self.assertEqual(response['message'], 'contrac and company created successfully')

        company = Company.query.filter_by(name='NewCompany').first()
        self.assertIsNotNone(company)

    def test_create_contrac_and_company_existing_company(self):
        """Prueba para cuando la empresa ya existe."""
        data = {
            'description': 'Test Contract',
            'start_date': '2024-01-01',
            'end_date': '2025-01-01',
            'name_company': 'TestCompany'  # Ya existe
        }

        response, status_code = create_contrac_and_company(data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], 'company already exists')

    def test_create_contrac_and_company_invalid_date_format(self):
        """Prueba para formato de fecha inválido."""
        data = {
            'description': 'Test Contract',
            'start_date': '01-01-2024',  # Formato incorrecto
            'end_date': '2025-01-01',
            'name_company': 'NewCompany'
        }

        response, status_code = create_contrac_and_company(data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], 'Invalid date format. Use YYYY-MM-DD')

if __name__ == '__main__':
    unittest.main()
