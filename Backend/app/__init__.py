from flask import Flask
from app.extensions import db, migrate, init_extensions
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_extensions(app)

    # Aquí inicializa Flask-Migrate
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "*"}})

    #with app.app_context():
        #db.create_all()

    # Registrar el blueprint de usuario
    from app.routes.usuario_routes import usuario_bp

    from app.routes.empresa_routes import empresa_bp
    from app.routes.incidente_routes import incidente_bp
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(empresa_bp, url_prefix='/api')
    app.register_blueprint(incidente_bp, url_prefix='/api')

    return app
