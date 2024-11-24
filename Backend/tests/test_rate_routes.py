from datetime import datetime
import unittest
from app import create_app, db
from app.models.models import Company, Contract, Rates

class RateServiceTestCase(unittest.TestCase):
    def setUp(self):
        # Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.company = Company(name="TestCompany")
        db.session.add(self.company)
        db.session.commit()

        self.contract = Contract(description="TestContract", start_date=datetime.now(), end_date=datetime.now(), company_id=self.company.id, plan="plan1")

    def tearDown(self):
        # Limpia después de cada prueba
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_rate_successful(self):
        # Prueba de creación exitosa de una tarifa
        data = {
            "rate": 100,
            "rate_per_incident": 10,
            "id_contract": 1,
            "source": "web"
        }
        response = self.client.post('/api/rate', json=data)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('rate created', response_data['message'])

    def test_create_rate_invalid_source(self):
        # Prueba de error por fuente inválida
        data = {
            "rate": 100,
            "rate_per_incident": 10,
            "id_contract": 1,
            "source": "invalid_source"
        }
        response = self.client.post('/api/rate', json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('source is invalid', response_data['message'])

    def test_get_all_rates(self):
        # Prueba de obtención de todas las tarifas
        # Crear algunas tarifas
        rate1 = Rates(rate=100, rate_per_incident=10, id_contract=1, source="web")
        rate2 = Rates(rate=200, rate_per_incident=20, id_contract=2, source="app")
        db.session.add(rate1)
        db.session.add(rate2)
        db.session.commit()

        response = self.client.get('/api/rates')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

    def test_get_rate_by_id_successful(self):
        # Prueba de obtención de una tarifa específica
        rate = Rates(rate=100, rate_per_incident=10, id_contract=1, source="web")
        db.session.add(rate)
        db.session.commit()

        response = self.client.get(f'/api/rate/{rate.id}')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['rate'], 100)

    def test_update_rate_successful(self):
        # Prueba de actualización exitosa
        rate = Rates(rate=100, rate_per_incident=10, id_contract=1, source="web")
        db.session.add(rate)
        db.session.commit()

        update_data = {"rate": 150, "rate_per_incident": 15}
        response = self.client.put(f'/api/rate/{rate.id}', json=update_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('rate updated', response_data['message'])

    def test_update_rate_not_found(self):
        # Prueba de actualización de tarifa no encontrada
        update_data = {"rate": 150, "rate_per_incident": 15}
        response = self.client.put('/api/rate/999', json=update_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('rate not found', response_data['message'])

    def test_delete_rate_successful(self):
        # Prueba de eliminación exitosa
        rate = Rates(rate=100, rate_per_incident=10, id_contract=1, source="web")
        db.session.add(rate)
        db.session.commit()

        response = self.client.delete(f'/api/rate/{rate.id}')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('rate deleted', response_data['message'])

    def test_delete_rate_not_found(self):
        # Prueba de eliminación de tarifa no encontrada
        response = self.client.delete('/api/rate/999')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('rate not found', response_data['message'])


if __name__ == '__main__':
    unittest.main()
