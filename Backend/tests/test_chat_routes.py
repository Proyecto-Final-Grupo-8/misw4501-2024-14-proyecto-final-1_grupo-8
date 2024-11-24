import unittest
from unittest.mock import patch
from flask import Flask
from app.routes.chat_route import magicloops_bp

class MagicLoopsTestCase(unittest.TestCase):
    def setUp(self):
        # Configuración de la aplicación Flask para pruebas
        self.app = Flask(__name__)
        self.app.register_blueprint(magicloops_bp)
        self.client = self.app.test_client()

    def tearDown(self):
        # Aquí puedes limpiar recursos si es necesario
        pass

    @patch('app.services.chat.ChatService.send_message_to_magicloops')
    def test_chat_with_magicloops_success(self, mock_chat_service):
        # Configura el mock para devolver una respuesta simulada
        mock_response = ({"message": "Hello from MagicLoops"}, 200)
        mock_chat_service.return_value = mock_response

        # Datos de entrada
        data = {"input": "Hello"}

        # Realiza la solicitud POST
        response = self.client.post('/chat', json=data)

        # Verifica la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello from MagicLoops"})

    @patch('app.services.chat.ChatService.send_message_to_magicloops')
    def test_chat_with_magicloops_error(self, mock_chat_service):
        # Configura el mock para devolver un error simulado
        mock_response = ({"error": "Something went wrong"}, 500)
        mock_chat_service.return_value = mock_response

        # Datos de entrada
        data = {"input": "Hello"}

        # Realiza la solicitud POST
        response = self.client.post('/chat', json=data)

        # Verifica la respuesta
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "Something went wrong"})

    @patch('app.services.chat.ChatService.send_message_to_magicloops')
    def test_chat_with_magicloops_missing_data(self, mock_chat_service):
        # Simula una respuesta cuando faltan datos
        mock_response = ({"error": "Invalid input data"}, 400)
        mock_chat_service.return_value = mock_response

        # Sin datos de entrada
        data = {}

        # Realiza la solicitud POST
        response = self.client.post('/chat', json=data)

        # Verifica la respuesta
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})


if __name__ == '__main__':
    unittest.main()
