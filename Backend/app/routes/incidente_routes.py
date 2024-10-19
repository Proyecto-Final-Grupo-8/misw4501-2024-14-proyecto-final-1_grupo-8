from flask import Blueprint, jsonify, request
from app.services.incidente_service import incidenteervice

incidente_bp = Blueprint('incidente', __name__)

@incidente_bp.route('/incidente', methods=['POST'])
def create_incidente():
    data = request.get_json()
    incidente = incidenteervice.create_incidente(data)
    return jsonify({"message": "incidente created", "incidente": incidente.id}), 201

@incidente_bp.route('/incidente', methods=['GET'])
def get_all_incidente():
    incidente = incidenteervice.get_all_incidente()
    return jsonify([incidente.serialize() for incidente in incidente]), 200

@incidente_bp.route('/incidente/<int:incidente_id>', methods=['GET'])
def get_incidente_by_id(incidente_id):
    incidente = incidenteervice.get_incidente_by_id(incidente_id)
    return jsonify(incidente.serialize()), 200

@incidente_bp.route('/incidente/<int:incidente_id>/logs', methods=['POST'])
def create_incidente_log(incidente_id):
    data = request.get_json()
    log = incidenteervice.create_incidente_log(incidente_id, data)
    return jsonify({"message": "incidente log created", "log": log.id}), 201

@incidente_bp.route('/incidente/<int:incidente_id>/logs', methods=['GET'])
def get_logs_for_incidente(incidente_id):
    logs = incidenteervice.get_logs_for_incidente(incidente_id)
    return jsonify([log.serialize() for log in logs]), 200
