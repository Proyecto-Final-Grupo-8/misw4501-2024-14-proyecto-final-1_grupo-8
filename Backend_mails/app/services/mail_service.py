from google.cloud import secretmanager
import imaplib
import email
import re
import json
from app.models.models import Users, Incident, IncidentLog  # Importar IncidentLog
from app.extensions import db  # Importar db correctamente

def get_secret():
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "projects/781163639586/secrets/Secret_Credentials/versions/latest"
        response = client.access_secret_version(request={"name": secret_name})
        secret_string = response.payload.data.decode("UTF-8")
        return json.loads(secret_string)
    except Exception as e:
        print(f"Error al obtener el secreto: {e}")
        return None

class MailService:
    @staticmethod
    def obtener_asuntos_remitentes_y_ids():
        mail_credentials = get_secret()
        if not mail_credentials:
            print("No se pudieron obtener las credenciales.")
            return []

        imap_server = 'imap.gmail.com'
        username = mail_credentials.get('MAIL_SERVICE')
        password = mail_credentials.get('MAIL_PASSWORD')
        emails_data = []

        try:
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(username, password)
            mail.select('inbox')

            # Buscar solo los mensajes no leídos
            status, messages = mail.search(None, 'UNSEEN')
            if status != 'OK':
                print("Error al buscar en la bandeja de entrada.")
                return []

            email_ids = messages[0].split()
            print("Número de correos no leídos:", len(email_ids))

            # Recorrer los IDs de los correos y obtener el asunto, remitente y cuerpo
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status != 'OK':
                    print(f"Error al obtener el mensaje con ID {email_id.decode()}")
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg.get("Subject", "Sin asunto")
                        from_email = msg.get("From", "Remitente desconocido")

                        match = re.search(r'<([^>]+)>', from_email)
                        email_address = match.group(1) if match else from_email

                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))


                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore').strip()
                                    break
                        else:
                            # Si no es multipart, intentamos obtener el contenido directamente
                            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore').strip()

                        # Validar si el correo pertenece a un usuario registrado
                        usuario = Users.query.filter_by(email=email_address).first()
                        if usuario:
                            print(f"Correo encontrado: {email_address}, ID de usuario: {usuario.id}")

                            # Crear un nuevo incidente
                            nuevo_incidente = Incident(
                                description=subject,
                                source="email",
                                customer_id=usuario.id
                            )
                            db.session.add(nuevo_incidente)
                            db.session.commit() 

                            # Crear un log asociado al incidente
                            nuevo_log = IncidentLog(
                                details=body,  
                                users_id=usuario.id,
                                incident_id=nuevo_incidente.id
                            )
                            db.session.add(nuevo_log)
                            db.session.commit()  
                            print(f"Incidente y log creados para el usuario {usuario.id}")

                            emails_data.append([email_id.decode(), subject, email_address, usuario.id])
                        else:
                            print(f"Correo no encontrado en la base de datos: {email_address}")

        except Exception as e:
            print(f"Error al acceder a la bandeja de entrada: {e}")
        finally:
            if 'mail' in locals():
                mail.logout()  # Cerrar la conexión

        return emails_data
