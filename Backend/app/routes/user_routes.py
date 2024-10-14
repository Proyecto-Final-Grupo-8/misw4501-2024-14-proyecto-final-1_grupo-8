# app/routes/user_routes.py

from flask import Blueprint, jsonify, request
from app.services.user_service import create_user, authenticate_user, get_user_info
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

# Registro de un nuevo usuario
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return create_user(data)

# Autenticación de un usuario (login)
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authenticate_user(data)

# Obtener la información del usuario autenticado
@user_bp.route('/user_info', methods=['GET'])
@jwt_required()
def user_info():
    current_user_id = get_jwt_identity()
    return get_user_info(current_user_id)


@user_bp.route('/ping', methods=['GET'])
def user_ping():
    return {"message": "health"}
