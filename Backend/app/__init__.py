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

    # Registrar el blueprint de users
    from app.routes.users_routes import users_bp
    from app.routes.company_routes import company_bp
    from app.routes.incident_routes import incident_bp
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(company_bp, url_prefix='/api')
    app.register_blueprint(incident_bp, url_prefix='/api')

    return app
