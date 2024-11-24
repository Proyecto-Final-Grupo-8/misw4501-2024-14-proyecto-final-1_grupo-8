from flask import Blueprint
from .users_routes import users_bp
from .company_routes import company_bp
from .incident_routes import incident_bp  # Importar las nuevas rutas
from .chat_route import magicloops_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(company_bp)
api_bp.register_blueprint(incident_bp)
api_bp.register_blueprint(magicloops_bp)
