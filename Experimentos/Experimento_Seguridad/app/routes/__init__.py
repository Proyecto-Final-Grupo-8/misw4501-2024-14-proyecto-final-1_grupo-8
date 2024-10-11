from .user_routes import user_bp

def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/api')
