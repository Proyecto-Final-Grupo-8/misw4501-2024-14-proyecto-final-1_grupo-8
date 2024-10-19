from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
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

    incidente = IncidenteService.create_incidente(nuevo_incidente)
    return jsonify({"message": "incidente created", "incidente": nuevo_incidente.id}), 201

@incidente_bp.route('/incidente', methods=['GET'])
def get_all_incidente():
    incidente = IncidenteService.get_all_incidente()
    return jsonify([incidente.serialize() for incidente in incidente]), 200

@incidente_bp.route('/incidente/<int:incidente_id>', methods=['GET'])
def get_incidente_by_id(incidente_id):
    incidente = IncidenteService.get_incidente_by_id(incidente_id)
    return jsonify(incidente.serialize()), 200

@incidente_bp.route('/incidente/<int:incidente_id>/logs', methods=['POST'])
def create_incidente_log(incidente_id):
    data = request.get_json()
    log = IncidenteService.create_incidente_log(incidente_id, data)
    return jsonify({"message": "incidente log created", "log": log.id}), 201

@incidente_bp.route('/incidente/<int:incidente_id>/logs', methods=['GET'])
def get_logs_for_incidente(incidente_id):
    logs = IncidenteService.get_logs_for_incidente(incidente_id)
    return jsonify([log.serialize() for log in logs]), 200
