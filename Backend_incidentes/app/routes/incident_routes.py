from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.models import IncidentLog, Users
from app.services.incident_service import IncidentService, Incident

incident_bp = Blueprint('incident', __name__)

@incident_bp.route('/incident', methods=['POST'])
@jwt_required()
def create_incident():
    user_id = get_jwt_identity()
    data = request.json

    if not data.get('description'):
        return jsonify({"message": "description is required"}), 400
    
    if data.get('source') not in ['web', 'app', 'telefono', 'email']:
        return jsonify({"message": "source is invalid"}), 400

    nuevo_incident = Incident(
        description=data.get('description'), 
        customer_id=user_id,
        source=data.get('source')
    )

    IncidentService.create_incident(nuevo_incident)
    return jsonify({"message": "incident created", "incident": nuevo_incident.id}), 201

@incident_bp.route('/incidents', methods=['GET'])
@jwt_required()
def get_all_incident():
    user_id = get_jwt_identity()
    users = db.session.get(Users, user_id)

    if not users:
        return jsonify({"message": "users not found"}), 404
    
    incident_obj = IncidentService.get_all_incident(user_id=user_id, user_role=users.role)
    return jsonify([incident.serialize() for incident in incident_obj]), 200


@incident_bp.route('/incident/<string:incident_id>', methods=['GET'])
@jwt_required()
def get_incident_by_id(incident_id):
    user_id = get_jwt_identity()
    users = db.session.get(Users, user_id)

    if not users:
        return jsonify({"message": "users not found"}), 404
        
    incident_obj = IncidentService.get_incident_by_id(user_id,users.role,incident_id)
    if not incident_obj:
        return jsonify({"message": "incident not found"}), 404
    return jsonify(incident_obj.serialize()), 200

@incident_bp.route('/incident/<string:incident_id>', methods=['PUT'])
@jwt_required()
def update_incident(incident_id):
    user_id = get_jwt_identity()
    data = request.json
    users = db.session.get(Users, user_id)
    incident_obj = Incident.query.filter_by(id=incident_id).first()
    
    if not incident_obj:
        return jsonify({"message": "incident not found"}), 404
    
    if users.role != 'analyst' and users.role != 'admin':
        return jsonify({"message": "you are not allowed to update this incident"}), 403
    
    if users.role == 'analyst' and data.get('status') not in ['Open', 'Progress', 'Closed', 'Rejected', 'Escalated', 'Canceled']:
        return jsonify({"message": "invalid status"}), 400
    
    IncidentService.update_incident(users.role,incident_id, data)  
    return jsonify({"message": "incident updated"}), 200

@incident_bp.route('/incident/<string:incident_id>', methods=['DELETE'])
@jwt_required()
def delete_incident(incident_id):
    user_id = get_jwt_identity()
    users = db.session.get(Users, user_id)
    incident_obj = Incident.query.filter_by(id=incident_id).first()

    if not incident_obj:
        return jsonify({"message": "incident not found"}), 404
    
    if users.role != 'admin':
        return jsonify({"message": "you are not allowed to delete this incident"}), 403
    
    IncidentService.delete_incident(incident_id)
    return jsonify({"message": "incident deleted"}), 200


@incident_bp.route('/incident/<string:incident_id>/logs', methods=['POST'])
@jwt_required()
def create_incident_log(incident_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    users= db.session.get(Users, user_id)
    Incident_obj = Incident.query.filter_by(id=incident_id, customer_id=user_id).first()

    if not data.get('details'):
        return jsonify({"message": "detail is required"}), 400
    
    if not users:
        return jsonify({"message": "users not found"}), 404
    
    if users.role == 'customer':
        if not Incident_obj:
            return jsonify({"message": "incident not found"}), 404

    nuevo_log = IncidentLog(
        details=data.get('details'),
        incident_id=incident_id,
        users_id=user_id        
    )

    log=IncidentService.create_incident_log(nuevo_log)
    return jsonify({"message": "incident log created", "log": log.id}), 201


@incident_bp.route('/incident/<string:incident_id>/logs', methods=['GET'])
@jwt_required()
def get_logs_for_incident(incident_id):
    user_id = get_jwt_identity()
    users = db.session.get(Users, user_id)
    Incident_obj = Incident.query.filter_by(id=incident_id).first()

    if not users:
        return jsonify({"message": "users not found"}), 404
    
    if not Incident_obj:
        return jsonify({"message": "incident not found"}), 404

    logs = IncidentService.get_logs_for_incident(incident_id)
    return jsonify([log.serialize() for log in logs]), 200

@incident_bp.route('/incident/<string:incident_id>/logs/<string:log_id>', methods=['GET'])
@jwt_required()
def get_log_by_id(incident_id, log_id):
    user_id = get_jwt_identity()
    users = db.session.get(Users, user_id)
    Incident_obj = Incident.query.filter_by(id=incident_id).first()
    log_obj = IncidentLog.query.filter_by(id=log_id).first()

    if not users:
        return jsonify({"message": "users not found"}), 404
    
    if not Incident_obj:
        return jsonify({"message": "incident not found"}), 404
    
    if not log_obj:
        return jsonify({"message": "log not found"}), 404

    return jsonify(log_obj.serialize()), 200

@incident_bp.route('/incident/<string:incident_id>/logs/<string:log_id>', methods=['PUT'])
@jwt_required()
def update_log(incident_id, log_id):
    user_id = get_jwt_identity()
    data = request.json
    users = db.session.get(Users, user_id)
    Incident_obj = Incident.query.filter_by(id=incident_id).first()
    log_obj = IncidentLog.query.filter_by(id=log_id).first()

    if not users:
        return jsonify({"message": "users not found"}), 404
    
    if not Incident_obj:
        return jsonify({"message": "incident not found"}), 404
    
    if not log_obj:
        return jsonify({"message": "log not found"}), 404

    IncidentService.update_log(log_id, data)
    return jsonify({"message": "log updated"}), 200

@incident_bp.route('/incident/<string:incident_id>/logs/<string:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(incident_id, log_id):
    user_id = get_jwt_identity()
    users = db.session.get(Users, user_id)
    Incident_obj = Incident.query.filter_by(id=incident_id).first()
    log_obj = IncidentLog.query.filter_by(id=log_id).first()

    if not users:
        return jsonify({"message": "users not found"}), 404
    
    if not Incident_obj:
        return jsonify({"message": "incident not found"}), 404
    
    if not log_obj:
        return jsonify({"message": "log not found"}), 404

    IncidentService.delete_log(log_id)
    return jsonify({"message": "log deleted"}), 200