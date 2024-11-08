from flask import Blueprint

from .incident_routes import incident_bp  # Importar las nuevas rutas

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(incident_bp)  # Registrar las rutas de incident
