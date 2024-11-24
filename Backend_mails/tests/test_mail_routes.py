import unittest
from unittest.mock import patch, MagicMock
from app.services.mail_service import MailService
from app.routes.mail_routes import mail_bp
from flask import Flask


class TestMailService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(mail_bp, url_prefix="/api")
        self.client = self.app.test_client()

        self.mock_secret = {
            'MAIL_SERVICE': 'testuser@gmail.com',
            'MAIL_PASSWORD': 'testpassword'
        }

    @patch('app.services.mail_service.get_secret')
    @patch('imaplib.IMAP4_SSL')
    def test_obtener_asuntos_remitentes_y_ids_no_secret(self, mock_imap, mock_get_secret):
        mock_get_secret.return_value = None

        emails_data = MailService.obtener_asuntos_remitentes_y_ids()
        self.assertEqual(emails_data, [])
        mock_imap.assert_not_called()

    @patch('app.services.mail_service.get_secret')
    @patch('imaplib.IMAP4_SSL')
    def test_obtener_asuntos_remitentes_y_ids_imap_error(self, mock_imap, mock_get_secret):
        mock_get_secret.return_value = self.mock_secret
        mock_imap.side_effect = Exception("IMAP connection error")

        emails_data = MailService.obtener_asuntos_remitentes_y_ids()
        self.assertEqual(emails_data, [])

    @patch('app.services.mail_service.MailService.obtener_asuntos_remitentes_y_ids')
    def test_procesar_correos_endpoint_success(self, mock_obtener_asuntos):
        mock_obtener_asuntos.return_value = [["1", "Test Subject", "testuser@example.com", 1]]

        with self.app.test_client() as client:
            response = client.post('/api/get-emails')
            self.assertEqual(response.status_code, 200)
            self.assertIn("emails", response.get_json())

    @patch('app.services.mail_service.MailService.obtener_asuntos_remitentes_y_ids')
    def test_procesar_correos_endpoint_error(self, mock_obtener_asuntos):
        mock_obtener_asuntos.side_effect = Exception("Processing error")

        with self.app.test_client() as client:
            response = client.post('/api/get-emails')
            self.assertEqual(response.status_code, 500)
            self.assertIn("error", response.get_json())


    @patch('app.services.mail_service.get_secret')
    @patch('imaplib.IMAP4_SSL')
    @patch('app.services.mail_service.Users.query')
    @patch('app.services.mail_service.db.session')
    def test_obtener_asuntos_remitentes_y_ids_multipart(
        self, mock_db_session, mock_users_query, mock_imap, mock_get_secret
    ):
        # Mock del secreto
        mock_get_secret.return_value = {
            'MAIL_SERVICE': 'test@example.com',
            'MAIL_PASSWORD': 'password'
        }

        # Mock del servidor IMAP
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        mock_mail.search.return_value = ('OK', [b'1'])
        
        # Mock del fetch, simulando un correo multipart
        mock_mail.fetch.return_value = (
            'OK', 
            [(b'1', b'From: testuser@example.com\r\nSubject: Test Subject\r\n\r\n--multipart_boundary\r\nContent-Type: text/plain\r\n\r\nPlain text content\r\n--multipart_boundary--')]
        )

        # Mock del mensaje multipart
        mock_msg = MagicMock()
        mock_msg.get.side_effect = lambda x, default=None: {
            'Subject': 'Multipart Subject',
            'From': 'testuser@example.com'
        }.get(x, default)
        mock_msg.is_multipart.return_value = True
        mock_msg.get_payload.return_value = [
            MagicMock(get_payload=lambda: "Plain text content", get_content_type=lambda: "text/plain")
        ]

        with patch('email.message_from_bytes', return_value=mock_msg):
            # Simular usuario existente
            mock_user = MagicMock()
            mock_user.id = 1
            mock_users_query.filter_by.return_value.first.return_value = mock_user

            # Ejecutar la función
            emails_data = MailService.obtener_asuntos_remitentes_y_ids()

            # Validar la longitud de los correos procesados
            self.assertEqual(len(emails_data), 1)
            self.assertEqual(emails_data[0][1], "Multipart Subject")
            self.assertEqual(emails_data[0][2], "testuser@example.com")


    @patch('app.services.mail_service.get_secret')
    @patch('imaplib.IMAP4_SSL')
    @patch('app.services.mail_service.Users.query')
    @patch('app.services.mail_service.db.session')
    def test_obtener_asuntos_remitentes_y_ids_unregistered_sender(
        self, mock_db_session, mock_users_query, mock_imap, mock_get_secret
    ):
        # Mock del secreto
        mock_get_secret.return_value = {
            'MAIL_SERVICE': 'test@example.com',
            'MAIL_PASSWORD': 'password'
        }

        # Mock del servidor IMAP
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        mock_mail.search.return_value = ('OK', [b'1'])
        
        # Mock del fetch, simulando un correo de remitente desconocido
        mock_mail.fetch.return_value = (
            'OK', 
            [(b'1', b'From: unknown@example.com\r\nSubject: Unknown Sender\r\n\r\nEmail body content')]
        )

        # Mock del mensaje
        mock_msg = MagicMock()
        mock_msg.get.side_effect = lambda x, default=None: {
            'Subject': 'Unknown Sender',
            'From': 'unknown@example.com'
        }.get(x, default)
        mock_msg.is_multipart.return_value = False
        mock_msg.get_payload.return_value = "Email body content"

        with patch('email.message_from_bytes', return_value=mock_msg):
            # Simular usuario inexistente
            mock_users_query.filter_by.return_value.first.return_value = None

            # Ejecutar la función
            emails_data = MailService.obtener_asuntos_remitentes_y_ids()

            # Validar que no se procese el correo
            self.assertEqual(emails_data, [])

    @patch('app.services.mail_service.get_secret')
    @patch('imaplib.IMAP4_SSL')
    def test_obtener_asuntos_remitentes_y_ids_processing_error(self, mock_imap, mock_get_secret):
        mock_get_secret.return_value = {
            'MAIL_SERVICE': 'test@example.com',
            'MAIL_PASSWORD': 'password'
        }

        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        mock_mail.search.return_value = ('OK', [b'1'])

        # Simular un error al procesar el correo
        mock_mail.fetch.side_effect = Exception("Unexpected processing error")

        emails_data = MailService.obtener_asuntos_remitentes_y_ids()

        # Validar que no se procesen correos
        self.assertEqual(emails_data, [])


if __name__ == "__main__":
    unittest.main()
