import unittest
from app import create_app, db
from flask_jwt_extended import create_access_token

class GraphQLTestCase(unittest.TestCase):
    def setUp(self):
        # Configura el entorno de prueba antes de cada test
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crear un token de prueba
        self.test_user_id = 1
        self.token = create_access_token(identity=self.test_user_id)

    def tearDown(self):
        # Limpia después de cada prueba
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_graphql_query_successful(self):
        # Prueba una consulta exitosa a /api/graphql-query
        query = """
        query {
        incidents {
            id
            description
            createdDate
        }
        }
        """
        data = {"query": query}
        response = self.client.post(
            '/api/graphql-query',
            json=data,
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response_data)
        self.assertIn("incidents", response_data["data"])

    def test_graphql_query_with_errors(self):
        # Prueba una consulta con errores sintácticos
        query = """
        query {
            invalidQuery {
                id
            }
        }
        """
        data = {"query": query}
        response = self.client.post(
            '/api/graphql-query',
            json=data,
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response_data)

    def test_graphql_endpoint(self):
        # Prueba el endpoint /api/graphql con una consulta válida
        query = """
        query {
            incidents {
                id
                description
                createdDate
            }
        }
        """
        data = {"query": query}
        response = self.client.post(
            '/api/graphql',
            json=data,
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response_data)

    def test_graphql_query_missing_auth(self):
        # Prueba el endpoint /api/graphql-query sin autenticación
        query = """
        query {
            allRates {
                id
                rate
                rate_per_incident
                source
            }
        }
        """
        data = {"query": query}
        response = self.client.post('/api/graphql-query', json=data)

        self.assertEqual(response.status_code, 401)
        self.assertIn("msg", response.get_json())
        self.assertEqual(response.get_json()["msg"], "Missing Authorization Header")

    def test_graphql_missing_auth(self):
        # Prueba el endpoint /api/graphql sin autenticación
        query = """
        query {
            allRates {
                id
                rate
                rate_per_incident
                source
            }
        }
        """
        data = {"query": query}
        response = self.client.post('/api/graphql', json=data)

        self.assertEqual(response.status_code, 200)  # No requiere autenticación por diseño
        response_data = response.get_json()
        self.assertIn("data", response_data)

if __name__ == "__main__":
    unittest.main()
