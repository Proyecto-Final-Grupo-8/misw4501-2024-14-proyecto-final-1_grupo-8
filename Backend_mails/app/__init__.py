from flask import Flask
from app.extensions import db, migrate, init_extensions
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.cloud import secretmanager
import os

# Importa tus modelos correctamente
from app.models.models import Users, Incident, IncidentLog

# Configura Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_secret(secret_name, project_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

def create_app(config_name=None):
    app = Flask(__name__)

    # Configuración del entorno
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Config')

    # Inicializa las extensiones
    init_extensions(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Importa y registra los blueprints
    from app.routes.mail_routes import mail_bp
    from app.routes.status_routes import status_bp

    app.register_blueprint(mail_bp, url_prefix='/api')
    app.register_blueprint(status_bp)

    return app
