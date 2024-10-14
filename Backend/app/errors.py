from flask import jsonify

def register_error_handlers(app):
    # Manejador para error 404 (Recurso no encontrado)
    @app.errorhandler(404)
    def not_found_error(error):
        response = {
            "error": "Not Found",
            "message": "The requested resource could not be found.",
            "status_code": 404
        }
        return jsonify(response), 404
    

    # Manejador para error 500 (Error Interno del Servidor)
    @app.errorhandler(500)
    def internal_server_error(error):
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
            "status_code": 500
        }
        return jsonify(response), 500

    # Manejador para excepciones genéricas (cualquier otro error)
    @app.errorhandler(Exception)
    def handle_exception(e):
        response = {
            "error": type(e).__name__,
            "message": str(e),
            "status_code": 500
        }
        return jsonify(response), 500
