from flask import Flask
from app.extensions import db, migrate, init_extensions
from flask_cors import CORS

def create_app(config_name=None):
    app = Flask(__name__)

    # Configuración del entorno
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Config')

    init_extensions(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Importa y registra los blueprints

    from app.routes.incident_routes import incident_bp
    from app.routes.status_routes import status_bp
    app.register_blueprint(incident_bp, url_prefix='/api')
    app.register_blueprint(status_bp)


    return app
