from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.models import IncidenteLog, Usuario
from app.services.incidente_service import IncidenteService, Incidente

incidente_bp = Blueprint('incidente', __name__)

@incidente_bp.route('/incidente', methods=['POST'])
@jwt_required()
def create_incidente():
    user_id = get_jwt_identity()
    data = request.json

    if not data.get('descripcion'):
        return jsonify({"message": "descripcion is required"}), 400
    
    if data.get('fuente') not in ['web', 'app', 'telefono', 'email']:
        return jsonify({"message": "fuente is invalid"}), 400

    nuevo_incidente = Incidente(
        descripcion=data.get('descripcion'), 
        cliente_id=user_id,
        fuente=data.get('fuente')
    )

    IncidenteService.create_incidente(nuevo_incidente)
    return jsonify({"message": "incidente created", "incidente": nuevo_incidente.id}), 201

@incidente_bp.route('/incidentes', methods=['GET'])
@jwt_required()
def get_all_incidente():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"message": "usuario not found"}), 404
    
    incidente_obj = IncidenteService.get_all_incidente(user_id=user_id, user_role=usuario.role)
    return jsonify([incidente.serialize() for incidente in incidente_obj]), 200


@incidente_bp.route('/incidente/<int:incidente_id>', methods=['GET'])
@jwt_required()
def get_incidente_by_id(incidente_id):
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"message": "usuario not found"}), 404
        
    incidente_obj = IncidenteService.get_incidente_by_id(user_id,usuario.role,incidente_id)
    if not incidente_obj:
        return jsonify({"message": "incidente not found"}), 404
    return jsonify(incidente_obj.serialize()), 200

@incidente_bp.route('/incidente/<int:incidente_id>', methods=['PUT'])
@jwt_required()
def update_incidente(incidente_id):
    user_id = get_jwt_identity()
    data = request.json
    usuario = Usuario.query.get(user_id)
    incidente_obj = Incidente.query.filter_by(id=incidente_id).first()
    
    if not incidente_obj:
        return jsonify({"message": "incidente not found"}), 404
    
    if usuario.role != 'analista':
        return jsonify({"message": "you are not allowed to update this incident"}), 403
    
    if data.get('estado') not in ['pendiente', 'en progreso', 'resuelto']:
        return jsonify({"message": "invalid estado"}), 400
    
    IncidenteService.update_incidente(incidente_id, data)  
    return jsonify({"message": "incidente updated"}), 200

@incidente_bp.route('/incidente/<int:incidente_id>/logs', methods=['POST'])
@jwt_required()
def create_incidente_log(incidente_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    usuario= Usuario.query.get(user_id)
    Incidente_obj = Incidente.query.filter_by(id=incidente_id, cliente_id=user_id).first()

    if not data.get('detalle'):
        return jsonify({"message": "detail is required"}), 400
    
    if not usuario:
        return jsonify({"message": "usuario not found"}), 404
    
    if usuario.role == 'cliente':
        if not Incidente_obj:
            return jsonify({"message": "incidente not found"}), 404

    nuevo_log = IncidenteLog(
        detalle=data.get('detalle'),
        incidente_id=incidente_id,
        usuario_id=user_id        
    )

    log=IncidenteService.create_incidente_log(nuevo_log)
    return jsonify({"message": "incidente log created", "log": log.id}), 201

