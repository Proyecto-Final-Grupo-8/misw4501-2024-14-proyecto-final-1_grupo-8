from flask import Blueprint, jsonify, request
from app.services.user_service import create_user, authenticate_user, get_user_info
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return create_user(data)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authenticate_user(data)

@user_bp.route('/user_info', methods=['GET'])
@jwt_required()
def user_info():
    current_user = get_jwt_identity()
    return get_user_info(current_user)
