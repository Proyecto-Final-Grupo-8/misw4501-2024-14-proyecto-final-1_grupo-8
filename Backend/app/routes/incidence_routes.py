from flask import Blueprint, jsonify, request
from app.services.incidence_service import IncidenceService

incidence_bp = Blueprint('incidences', __name__)

@incidence_bp.route('/incidences', methods=['POST'])
def create_incidence():
    data = request.get_json()
    incidence = IncidenceService.create_incidence(data)
    return jsonify({"message": "Incidence created", "incidence": incidence.id}), 201

@incidence_bp.route('/incidences', methods=['GET'])
def get_all_incidences():
    incidences = IncidenceService.get_all_incidences()
    return jsonify([incidence.serialize() for incidence in incidences]), 200

@incidence_bp.route('/incidences/<int:incidence_id>', methods=['GET'])
def get_incidence_by_id(incidence_id):
    incidence = IncidenceService.get_incidence_by_id(incidence_id)
    return jsonify(incidence.serialize()), 200

@incidence_bp.route('/incidences/<int:incidence_id>/logs', methods=['POST'])
def create_incidence_log(incidence_id):
    data = request.get_json()
    log = IncidenceService.create_incidence_log(incidence_id, data)
    return jsonify({"message": "Incidence log created", "log": log.id}), 201

@incidence_bp.route('/incidences/<int:incidence_id>/logs', methods=['GET'])
def get_logs_for_incidence(incidence_id):
    logs = IncidenceService.get_logs_for_incidence(incidence_id)
    return jsonify([log.serialize() for log in logs]), 200
