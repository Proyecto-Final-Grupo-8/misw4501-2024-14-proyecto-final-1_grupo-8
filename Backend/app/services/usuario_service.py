# app/services/usuario_service.py

from app.models.models import usuario, empresa, contrato
from app import db
from flask_jwt_extended import create_access_token
import datetime

def create_usuario(data):
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # Especificamos el rol
    empresa_id = data.get('empresa_id')  # Especificamos la empresa (para cliente y analista)

    # Validamos si el usuario ya existe
    if usuario.query.filter_by(username=username).first():
        return {'message': 'usuario already exists'}, 400

    # Validamos si el rol es válido
    if role not in ['empresa', 'cliente', 'analista']:
        return {'message': 'Invalid role specified'}, 400

    empresa_obj = None  # Aquí cambiamos el nombre de la variable local
    if role != 'empresa':
        empresa_obj = empresa.query.filter_by(id=empresa_id).first()
        if not empresa_obj:
            return {'message': 'empresa not found'}, 404

    # Creamos el nuevo usuario
    new_user = usuario(username=username, role=role, empresa=empresa_obj)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'usuario created successfully'}, 201

def authenticate_usuario(data):
    username = data.get('username')
    password = data.get('password')

    user = usuario.query.filter_by(username=username).first()

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

def get_usuario_info(usuario_id):
    usuario = usuario.query.get(usuario_id)

    if not usuario:
        return {'message': 'usuario not found'}, 404

    # Devolvemos la información del usuario, incluyendo su rol y empresa
    return {
        'username': usuario.username,
        'role': usuario.role,
        'empresa': usuario.empresa.nombre if usuario.empresa else None
    }, 200

def create_contrato_and_empresa(data):
    # Información del contrato
    descripcion = data.get('descripcion')
    fecha_inicio_str = data.get('fecha_inicio')
    fecha_fin_str = data.get('fecha_fin')
    nombre_empresa = data.get('nombre_empresa') 

    if not descripcion or not fecha_inicio_str or not fecha_fin_str or not nombre_empresa:
        return {'message': 'Missing data for contrato or empresa'}, 400

    try:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    except ValueError:
        return {'message': 'Invalid date format. Use YYYY-MM-DD'}, 400
    
    # Verificar si la empresa ya existe
    if empresa.query.filter_by(nombre=nombre_empresa).first():
        return {'message': 'empresa already exists'}, 400

    # Crear el contrato
    new_contrato = contrato(
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    
    db.session.add(new_contrato)
    db.session.commit()

    # Crear la empresa asociada
    new_empresa = empresa(
        nombre=nombre_empresa,
        contrato_id=new_contrato.id
    )

    db.session.add(new_empresa)
    db.session.commit()

    return {
        'message': 'contrato and empresa created successfully',
        'empresa_id': new_empresa.id,
        'contrato_id': new_contrato.id
    }, 201