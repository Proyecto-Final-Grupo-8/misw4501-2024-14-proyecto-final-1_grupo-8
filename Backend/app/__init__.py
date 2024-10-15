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

    with app.app_context():
        db.create_all()

    # Registrar el blueprint de usuario
    from app.routes.user_routes import user_bp
    from app.routes.empresa_routes import empresa_bp
    # from app.routes.incidence_routes import incidence_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(empresa_bp, url_prefix='/api')
    # app.register_blueprint(incidence_bp, url_prefix='/api')

    return app
