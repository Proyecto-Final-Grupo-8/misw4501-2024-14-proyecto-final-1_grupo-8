import datetime
import re
from flask import Blueprint, jsonify, request
from app.services.users_service import UsersService
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = {
        'role': 'role is required',
        'username': 'username is required',
        'password': 'password is required',
        'email': 'email is required',
        'phone': 'phone is required',
        'name': 'name is required',
        'last_name': 'last_name is required'
    }

    # Validar que cada campo requerido esté en data
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {'message': ', '.join([required_fields[field] for field in missing_fields])}, 400

    # Validaciones específicas para campos individuales
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
        return {'message': 'Invalid email'}, 400

    if not re.match(r"^\d{10,11}$", data.get('phone', '')):
        return {'message': 'Invalid phone number'}, 400

    if data.get('role') not in ['company', 'customer', 'analyst', 'admin']:
        return {'message': 'Invalid role specified'}, 400

    if not re.match(r"^[a-zA-Z\s]+$", data.get('name', '')):
        return {'message': 'Invalid name'}, 400

    if not re.match(r"^[a-zA-Z\s]+$", data.get('last_name', '')):
        return {'message': 'Invalid last name'}, 400

    return UsersService.create_users(data)

# Autenticación de un users (login)
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return UsersService.authenticate_users(data)

# Obtener la información del users autenticado
@users_bp.route('/user', methods=['GET'])
@jwt_required()
def users_info():
    current_users_id = get_jwt_identity()
    return UsersService.get_users_info(current_users_id)

@users_bp.route('user/<string:users_id>', methods=['GET'])
def get_users(users_id):
    return UsersService.get_users_info(users_id)

@users_bp.route('user/<string:users_id>', methods=['PUT'])
def update_users(users_id):
    data = request.json
    return UsersService.update_users(users_id, data)

@users_bp.route('user/<string:users_id>', methods=['DELETE'])
def delete_users(users_id):
    return UsersService.delete_users(users_id)

@users_bp.route('user/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_users_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_users_id, expires_delta=datetime.timedelta(hours=1))
    return jsonify(access_token=new_access_token), 200