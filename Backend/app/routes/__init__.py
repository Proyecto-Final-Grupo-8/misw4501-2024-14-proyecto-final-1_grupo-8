from flask import Blueprint
from .users_routes import users_bp
from .company_routes import company_bp
from .incident_routes import incident_bp  # Importar las nuevas rutas

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(company_bp)
api_bp.register_blueprint(incident_bp)  # Registrar las rutas de incident
