from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.models import IncidentLog, Users
from app.services.mail_service import MailService

mail_bp = Blueprint('mail', __name__)

# Define el endpoint utilizando el Blueprint
@mail_bp.route('/procesar-correos', methods=['POST'])
#@jwt_required()  # Descomenta esto si necesitas autenticar la solicitud
def procesar_correos_endpoint():
    try:
        # Llama a la función para obtener los asuntos y IDs de correos no leídos
        emails_data = MailService.obtener_asuntos_remitentes_y_ids()

        # Devuelve la respuesta en formato JSON
        return jsonify({"emails": emails_data}), 200
    except Exception as e:
        # Maneja cualquier excepción que ocurra
        return jsonify({"error": str(e)}), 500