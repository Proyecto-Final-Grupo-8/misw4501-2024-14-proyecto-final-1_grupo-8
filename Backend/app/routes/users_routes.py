import datetime
from flask import Blueprint, jsonify, request
from app.services.users_service import UsersService
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

users_bp = Blueprint('users_bp', __name__)

# Registro de un nuevo users
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
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