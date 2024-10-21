# app/services/users_service.py

from app.models.models import Users, Company, Contrac
from app import db
from flask_jwt_extended import create_access_token
import datetime

def create_users(data):
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # Especificamos el rol
    company_id = data.get('company_id')  # Especificamos la company (para customer y analyst)

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
    new_user = Users(username=username, role=role, company=company_obj)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'users created successfully'}, 201

def authenticate_users(data):
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return {'message': 'Invalid credentials'}, 401

    # Generamos el token de acceso
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))


    # Devolvemos el token, rol del users y la company a la que pertenece (si tiene)
    return {
        'access_token': access_token,
        'role': user.role,
        'company': user.company.name if user.company else None
    }, 200

def get_users_info(users_id):
    users = users.query.get(users_id)

    if not users:
        return {'message': 'users not found'}, 404

    # Devolvemos la información del users, incluyendo su rol y company
    return {
        'username': users.username,
        'role': users.role,
        'company': users.company.name if users.company else None
    }, 200

def create_contrac_and_company(data):
    # Información del contrac
    description = data.get('description')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    name_company = data.get('name_company') 

    if not description or not start_date_str or not end_date_str or not name_company:
        return {'message': 'Missing data for contrac or company'}, 400

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return {'message': 'Invalid date format. Use YYYY-MM-DD'}, 400
    
    # Verificar si la company ya existe
    if Company.query.filter_by(name=name_company).first():
        return {'message': 'company already exists'}, 400

    # Crear el contrac
    new_contrac = Contrac(
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    
    db.session.add(new_contrac)
    db.session.commit()

    # Crear la company asociada
    new_company = Company(
        name=name_company,
        contrac_id=new_contrac.id
    )

    db.session.add(new_company)
    db.session.commit()

    return {
        'message': 'contrac and company created successfully',
        'company_id': new_company.id,
        'contrac_id': new_contrac.id
    }, 201