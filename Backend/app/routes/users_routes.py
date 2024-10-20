from flask import Blueprint, jsonify, request
from app.services.users_service import create_users, authenticate_users, get_users_info
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users_bp', __name__)

# Registro de un nuevo users
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return create_users(data)

# Autenticación de un users (login)
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authenticate_users(data)

# Obtener la información del users autenticado
@users_bp.route('/users_info', methods=['GET'])
@jwt_required()
def users_info():
    current_users_id = get_jwt_identity()
    return get_users_info(current_users_id)


@users_bp.route('/ping', methods=['GET'])
def users_ping():
    return {"message": "health"}
