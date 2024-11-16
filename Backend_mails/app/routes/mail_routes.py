from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.services.mail_service import MailService

# Crea un Blueprint para el manejo de correos
mail_bp = Blueprint('mail', __name__)

# Define el endpoint utilizando el Blueprint
@mail_bp.route('/procesar-correos', methods=['POST'])
#@jwt_required()  # Requiere autenticación JWT
def procesar_correos_endpoint():
    service = MailService.obtener_servicio_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    
    return jsonify({"message": messages}), 200

