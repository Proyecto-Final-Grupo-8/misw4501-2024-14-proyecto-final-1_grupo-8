from flask import Blueprint

from .mail_routes import mail_bp  # Importar las nuevas rutas

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(mail_bp)  # Registrar las rutas de incident
