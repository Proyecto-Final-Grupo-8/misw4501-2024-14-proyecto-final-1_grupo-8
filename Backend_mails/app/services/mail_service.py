from flask import app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import secretmanager
import os
import re
import logging
from app.models.models import Users, Incident, IncidentLog  # Importa tus modelos correctamente
from app.extensions import db  # Importa la instancia de db correctamente


def get_secret(secret_name, project_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

# Configura Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class MailService:
    @staticmethod
    def obtener_servicio_gmail():
        # Configuración de Gmail API
        creds = None
        project_id = "781163639586"  # Reemplaza con tu ID de proyecto
        secret_name = "mail-credentias"  # Reemplaza con el nombre de tu secreto

        # Recupera las credenciales desde Secret Manager
        credentials_json = get_secret(secret_name, project_id)

        # Guarda temporalmente el archivo de credenciales en disco
        with open("credentials_temp.json", "w") as file:
            file.write(credentials_json)

        # Maneja las credenciales de Gmail API
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials_temp.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Guarda el token de acceso
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    @staticmethod
    def obtener_asuntos_remitentes_y_ids():

        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])

        if not messages:
            print("No hay mensajes no leídos.")
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                payload = msg['payload']
                headers = payload['headers']

                # Extraer el remitente y el asunto del correo
                remitente = next(header['value'] for header in headers if header['name'] == 'From')
                cuerpo_correo = payload['body']['data'] if 'data' in payload['body'] else "Sin contenido"

                # Decodificar el cuerpo del correo si es necesario
                if cuerpo_correo:
                    cuerpo_correo = base64.urlsafe_b64decode(cuerpo_correo).decode('utf-8', errors='ignore')

                # Procesar el correo
                procesar_correo(remitente, cuerpo_correo)

    # Procesar correo
    @staticmethod
    def procesar_correo(correo_remitente, cuerpo_correo):
        email_pattern = r'<([^>]+)>'
        match = re.search(email_pattern, correo_remitente)
        fixed_email = match.group(1) if match else correo_remitente  # Maneja el caso en que no haya coincidencia

        # Verificar si el remitente está registrado en la tabla Users
        usuario = Users.query.filter_by(email=fixed_email).first()

        if usuario:
            # Crear un nuevo incidente si el usuario existe
            nuevo_incidente = Incident(
                description=cuerpo_correo,
                source="email",
                customer_id=usuario.id
            )
            db.session.add(nuevo_incidente)
            db.session.commit()
            print("Incidente creado con éxito.")
            return "Incidente creado con éxito."
        else:
            print(f"{correo_remitente} El remitente no está registrado en la base de datos.")
            return "El remitente no está registrado en la base de datos."