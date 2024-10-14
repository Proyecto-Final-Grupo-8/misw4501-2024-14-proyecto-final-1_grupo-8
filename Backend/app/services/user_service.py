# app/services/user_service.py

from app.models.user import User
from app.models.empresas import Empresa
from app.models.contrato import Contrato
from app import db
from flask_jwt_extended import create_access_token
import datetime

def test_connection_db():
    return db.engine.execute("SELECT 1").fetchall()

def create_user(data):
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # Nuevo: Especificamos el rol
    empresa_id = data.get('empresa_id')  # Nuevo: Especificamos la empresa (para cliente y analista)

    # Validamos si el usuario ya existe
    if User.query.filter_by(username=username).first():
        return {'message': 'User already exists'}, 400

    # Validamos si el rol es válido
    if role not in ['empresa', 'cliente', 'analista']:
        return {'message': 'Invalid role specified'}, 400

    # Si el rol no es 'empresa', necesitamos asociar el usuario a una empresa existente
    if role != 'empresa':
        empresa = Empresa.query.filter_by(id=empresa_id).first()
        if not empresa:
            return {'message': 'Empresa not found'}, 404
    else:
        empresa = None  # Empresas no tienen empresa asociada

    # Creamos el nuevo usuario
    new_user = User(username=username, role=role, empresa=empresa)
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

    # Generamos el token de acceso
    access_token = create_access_token(identity=user.id)

    # Devolvemos el token, rol del usuario y la empresa a la que pertenece (si tiene)
    return {
        'access_token': access_token,
        'role': user.role,
        'empresa': user.empresa.nombre if user.empresa else None
    }, 200

def get_user_info(user_id):
    user = User.query.get(user_id)

    if not user:
        return {'message': 'User not found'}, 404

    # Devolvemos la información del usuario, incluyendo su rol y empresa
    return {
        'username': user.username,
        'role': user.role,
        'empresa': user.empresa.nombre if user.empresa else None
    }, 200

def create_contract_and_empresa(data):
    # Información del contrato
    descripcion = data.get('descripcion')
    fecha_inicio_str = data.get('fecha_inicio')
    fecha_fin_str = data.get('fecha_fin')
    nombre_empresa = data.get('nombre_empresa') 

    if not descripcion or not fecha_inicio_str or not fecha_fin_str or not nombre_empresa:
        return {'message': 'Missing data for contract or company'}, 400

    try:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    except ValueError:
        return {'message': 'Invalid date format. Use YYYY-MM-DD'}, 400
    
    # Verificar si la empresa ya existe
    if Empresa.query.filter_by(nombre=nombre_empresa).first():
        return {'message': 'Empresa already exists'}, 400

    # Crear el contrato
    new_contrato = Contrato(
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    
    db.session.add(new_contrato)
    db.session.commit()

    # Crear la empresa asociada
    new_empresa = Empresa(
        nombre=nombre_empresa,
        contrato_id=new_contrato.id
    )

    db.session.add(new_empresa)
    db.session.commit()

    return {
        'message': 'Contract and Empresa created successfully',
        'empresa_id': new_empresa.id,
        'contrato_id': new_contrato.id
    }, 201