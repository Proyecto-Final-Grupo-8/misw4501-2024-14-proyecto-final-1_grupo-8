import unittest
from app import create_app, db
from app.models import Company

class CompanyServiceTestCase(unittest.TestCase):
    def setUp(self):
        #Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        #Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_company_successful(self):
        #Prueba de creación de empresa exitosa.
        data = {
            'name': 'TestCompany'
        }
        response = self.client.post('/api/company', json=data)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('company created', response_data['message'])

    def test_create_company_missing_fields(self):
        #Prueba de error por campos faltantes en creación de empresa.
        data = {
            # Falta el campo name
        }
        response = self.client.post('/api/company', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('name is required', response_data['message'])

    def test_create_company_duplicate_name(self):
        #Prueba de error por nombre duplicado en creación de empresa.
        data = {
            'name': 'TestCompany'
        }
        response = self.client.post('/api/company', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('company already exists', response_data['message'])

    def test_get_companies(self):
        #Prueba de obtención de empresas.
        response = self.client.get('/api/company')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)

    def test_get_company(self):
        #Prueba de obtención de empresa.
        company = Company(name='TestCompany')
        db.session.add(company)
        db.session.commit()

        response = self.client.get(f'/api/company/{company.id}')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['name'], 'TestCompany')

    def test_get_company_not_found(self):
        #Prueba de error por empresa no encontrada.
        response = self.client.get('/api/company/1')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('company not found', response_data['message'])

    def test_update_company_successful(self):
        #Prueba de actualización de empresa exitosa.
        company = Company(name='TestCompany')
        db.session.add(company)
        db.session.commit()

        data = {
            'name': 'UpdatedCompany'
        }
        response = self.client.put(f'/api/company/{company.id}', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('company updated', response_data['message'])

    def test_update_company_missing_fields(self):
        #Prueba de error por campos faltantes en actualización de empresa.
        company = Company(name='TestCompany')
        db.session.add(company)
        db.session.commit()

        data = {
            # Falta el campo name
        }
        response = self.client.put(f'/api/company/{company.id}', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('name is required', response_data['message'])

    def test_update_company_duplicate_name(self):
        #Prueba de error por nombre duplicado en actualización de empresa.
        company1 = Company(name='TestCompany1')
        company2 = Company(name='TestCompany2')
        db.session.add_all([company1, company2])
        db.session.commit()

        data = {
            'name': 'TestCompany2'
        }
        response = self.client.put(f'/api/company/{company1.id}', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('company already exists', response_data['message'])

    def test_update_company_not_found(self):
        #Prueba de error por empresa no encontrada en actualización de empresa.
        data = {
            'name': 'UpdatedCompany'
        }
        response = self.client.put('/api/company/1', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('company not found', response_data['message'])

    def test_delete_company_successful(self):
        #Prueba de eliminación de empresa exitosa.
        company = Company(name='TestCompany')
        db.session.add(company)
        db.session.commit()

        response = self.client.delete(f'/api/company/{company.id}')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('company deleted', response_data['message'])

    def test_delete_company_not_found(self):
        #Prueba de error por empresa no encontrada en eliminación de empresa.
        response = self.client.delete('/api/company/1')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('company not found', response_data['message'])