# app/routes/empresa_routes.py

from flask import Blueprint, jsonify, request
from app.models.models import Empresa
from app import db
from app.services.usuario_service import create_contrato_and_empresa

empresa_bp = Blueprint('empresa_bp', __name__)

@empresa_bp.route('/register', methods=['POST'])
def register_empresa():
    data = request.get_json()
    nombre = data.get('nombre')
    contrato_id = data.get('contrato_id')  # Suponemos que el contrato ya está creado

    if Empresa.query.filter_by(nombre=nombre).first():
        return {'message': 'empresa already exists'}, 400

    new_empresa = Empresa(nombre=nombre, contrato_id=contrato_id)
    db.session.add(new_empresa)
    db.session.commit()

    return {'message': 'empresa created successfully'}, 201

@empresa_bp.route('/create_contract', methods=['POST'])
def create_contrato():
    data = request.get_json()
    return create_contrato_and_empresa(data)
