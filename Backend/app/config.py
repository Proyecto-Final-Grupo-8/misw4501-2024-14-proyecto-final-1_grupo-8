import os
from dotenv import load_dotenv
from google.cloud import secretmanager
import json

load_dotenv()

def get_db_credentials():

    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/781163639586/secrets/Secret_Credentials/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    secret_string = response.payload.data.decode("UTF-8")
    return json.loads(secret_string)

# Obtén las credenciales de la base de datos desde Secret Manager
db_credentials = get_db_credentials()

class Config:
    # Construye la URI de conexión utilizando las credenciales seguras
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_credentials['DB_USER']}:{db_credentials['DB_PASSWORD']}@" \
                              f"{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_NAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = db_credentials['JWT_SECRET_KEY']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True
