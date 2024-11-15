from flask import Blueprint, request, jsonify
from app.services.chat import ChatService

magicloops_bp = Blueprint('magicloops_bp', __name__)

@magicloops_bp.route('/chat', methods=['POST'])
def chat_with_magicloops():
    data = request.get_json()

    response, status = ChatService.send_message_to_magicloops(data)
    return jsonify(response), status
