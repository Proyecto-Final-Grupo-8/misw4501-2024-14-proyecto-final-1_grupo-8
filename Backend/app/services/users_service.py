# app/services/users_service.py

from app.models.models import Users, Company, Contract
from app import db
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime
import re

class UsersService:
    @staticmethod
    def create_users(data):
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')  # Especificamos el rol
        company_id = data.get('company_id')  # Especificamos la company (para customer y analyst)
        email = data.get('email')
        phone = data.get('phone')
        name = data.get('name')
        last_name = data.get('last_name')

        # Validamos si el users ya existe
        if Users.query.filter_by(username=username).first():
            return {'message': 'users already exists'}, 400

        # Validamos si el rol es válido
        if role not in ['company', 'customer', 'analyst', 'admin']:
            return {'message': 'Invalid role specified'}, 400

        company_obj = None  # Aquí cambiamos el name de la variable local
        if role != 'company':
            company_obj = Company.query.filter_by(id=company_id).first()
            if not company_obj:
                return {'message': 'company not found'}, 404
            
        # Creamos el nuevo users
        new_user = Users(username=username, role=role, company=company_obj, email=email, phone=phone, name=name, last_name=last_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'users created successfully'}, 201
    
    @staticmethod
    def authenticate_users(data):
        username = data.get('username')
        password = data.get('password')

        user = Users.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        # Generamos el token de acceso
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        refresh_token = create_refresh_token(identity=user.id)


        # Devolvemos el token, rol del users y la company a la que pertenece (si tiene)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'role': user.role,
            'company': user.company.name if user.company else None
        }, 200

    @staticmethod
    def get_users_info(users_id):
        users = Users.query.get(users_id)

        if not users:
            return {'message': 'users not found'}, 404

        # Devolvemos la información del users, incluyendo su rol y company
        return {
            'id': users.id,
            'username': users.username,
            'role': users.role,
            'company': users.company.name if users.company else None
        }, 200

    @staticmethod
    def delete_users(users_id):
        users = Users.query.get(users_id)

        if not users:
            return {'message': 'users not found'}, 404

        # Eliminamos el users
        db.session.delete(users)
        db.session.commit()

        return {'message': 'users deleted successfully'}, 200

    @staticmethod
    def update_users(users_id, data):
        users = Users.query.get(users_id)
        
        if not users:
            return {'message': 'users not found'}, 404
        
        if 'password' in data:
            new_password = data.get('password')
            
            if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,16}$', new_password):
                return {
                    'message': 'Password must be 8-16 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character'
                }, 400
            
            users.set_password(new_password)

        db.session.commit()

        return {'message': 'users updated successfully'}, 200
