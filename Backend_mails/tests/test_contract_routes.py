from datetime import datetime
import unittest
from app import create_app, db
from app.models import Contract, Company

class ContractServiceTestCase(unittest.TestCase):
    def setUp(self):
        #Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        #Crear compañía para asociar con contratos en pruebas
        self.company = Company(name="TestCompany")
        db.session.add(self.company)
        db.session.commit()
  
    def tearDown(self):
        #Limpia después de cada prueba.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_contract_successful(self):
       
        #Prueba de creación de contrato exitosa.
        data = {
            'description': 'TestContract',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.post('/api/contract', json=data)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('contract created', response_data['message'])

    def test_create_contract_missing_fields(self):
        #Prueba de error por campos faltantes en creación de contrato.
        data = {
            # Falta el campo description
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.post('/api/contract', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('description is required', response_data['message'])

    def test_get_contracts(self):
        #Prueba de obtención de contratos.
        response = self.client.get('/api/contracts')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)

    def test_get_contract(self):
        #Crear un contrato para obtener en pruebas
        data = {
            'description': 'TestContract',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.post('/api/contract', json=data)
        response_data = response.get_json()
        contract_id = response_data.get('contract')

        response = self.client.get(f'/api/contract/{contract_id}')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['description'], 'TestContract')
    
    def test_get_contract_not_found(self):
        #Prueba de error por contrato no encontrado.
        response = self.client.get('/api/contract/XXXX')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_update_contract(self):
        #Prueba de actualización de contrato.
        data = {
            'description': 'TestContract',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.post('/api/contract', json=data)
        response_data = response.get_json()
        contract_id = response_data.get('contract')

        data = {
            'description': 'TestContractUpdated',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.put(f'/api/contract/{contract_id}', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('contract updated', response_data['message'])

    def test_update_contract_not_found(self):
        #Prueba de error por contrato no encontrado en actualización de contrato.
        data = {
            'description': 'TestContract',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.put('/api/contract/XXXX', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_delete_contract(self):
        #Prueba de eliminación de contrato.
        data = {
            'description': 'TestContract',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'company_id': self.company.id,
            'plan': 'plan1'
        }
        response = self.client.post('/api/contract', json=data)
        response_data = response.get_json()
        contract_id = response_data.get('contract')

        response = self.client.delete(f'/api/contract/{contract_id}')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('contract deleted', response_data['message'])


if __name__ == '__main__':
    unittest.main()


    