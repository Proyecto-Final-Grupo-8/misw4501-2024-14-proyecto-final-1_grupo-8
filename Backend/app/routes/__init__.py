from flask import Blueprint
from .user_routes import user_bp
from .empresa_routes import empresa_bp
from .incidence_routes import incidence_bp  # Importar las nuevas rutas

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(empresa_bp)
api_bp.register_blueprint(incidence_bp)  # Registrar las rutas de incidencias
