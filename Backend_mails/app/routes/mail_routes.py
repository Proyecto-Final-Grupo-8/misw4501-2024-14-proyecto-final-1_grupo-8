from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.models import IncidentLog, Users
from app.services.mail_service import MailService

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/get-emails', methods=['POST'])
#@jwt_required()
def procesar_correos_endpoint():
    try:
        emails_data = MailService.obtener_asuntos_remitentes_y_ids()
        return jsonify({"emails": emails_data}), 200
    except Exception as e:

        return jsonify({"error": str(e)}), 500