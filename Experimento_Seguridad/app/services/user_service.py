from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token

def create_user(data):
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return {'message': 'User already exists'}, 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User created successfully'}, 201

def authenticate_user(data):
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return {'message': 'Invalid credentials'}, 401

    access_token = create_access_token(identity=user.id)
    return {'access_token': access_token}, 200

def get_user_info(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, 404

    return {'username': user.username}, 200
