from flask import Blueprint, jsonify, request
from app.services.usuario_service import create_usuario, authenticate_usuario, get_usuario_info
from flask_jwt_extended import jwt_required, get_jwt_identity

usuario_bp = Blueprint('usuario_bp', __name__)

# Registro de un nuevo usuario
@usuario_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return create_usuario(data)

# Autenticación de un usuario (login)
@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authenticate_usuario(data)

# Obtener la información del usuario autenticado
@usuario_bp.route('/usuario_info', methods=['GET'])
@jwt_required()
def usuario_info():
    current_usuario_id = get_jwt_identity()
    return get_usuario_info(current_usuario_id)


@usuario_bp.route('/ping', methods=['GET'])
def usuario_ping():
    return {"message": "health"}
