from flask import Blueprint
from .usuario_routes import usuario_bp
from .empresa_routes import empresa_bp
from .incidente_routes import incidente_bp  # Importar las nuevas rutas

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(usuario_bp)
api_bp.register_blueprint(empresa_bp)
api_bp.register_blueprint(incidente_bp)  # Registrar las rutas de incidente
