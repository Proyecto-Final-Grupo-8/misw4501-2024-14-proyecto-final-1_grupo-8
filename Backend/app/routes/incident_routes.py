import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import requests
from google.cloud import secretmanager

incident_bp = Blueprint('incident', __name__)

# Define la URL base externa
def get_secret():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/781163639586/secrets/Secret_Credentials/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    secret_str = response.payload.data.decode("UTF-8")
    return json.loads(secret_str)

get_credentials = get_secret()
external_url_base = get_credentials["LB_INCIDENTS"]

# Función para redirigir solicitudes
def forward_request_to_external(url, method, data=None):
    headers = {"Authorization": request.headers.get("Authorization")}
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, json=data, headers=headers)
    elif method == 'PUT':
        response = requests.put(url, json=data, headers=headers)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        return jsonify({"message": "Invalid method"}), 405

    return jsonify(response.json()), response.status_code

@incident_bp.route('/incident', methods=['POST'])
@jwt_required()
def create_incident():
    return forward_request_to_external(f'{external_url_base}/incident', 'POST', request.json)

@incident_bp.route('/incidents', methods=['GET'])
@jwt_required()
def get_all_incident():
    return forward_request_to_external(f'{external_url_base}/incidents', 'GET')

@incident_bp.route('/incident/<string:incident_id>', methods=['GET'])
@jwt_required()
def get_incident_by_id(incident_id):
    url = f"{external_url_base}/incident/{incident_id}"
    return forward_request_to_external(url, 'GET')

@incident_bp.route('/incident/<string:incident_id>', methods=['PUT'])
@jwt_required()
def update_incident(incident_id):
    url = f"{external_url_base}/incident/{incident_id}"
    return forward_request_to_external(url, 'PUT', request.json)

@incident_bp.route('/incident/<string:incident_id>', methods=['DELETE'])
@jwt_required()
def delete_incident(incident_id):
    url = f"{external_url_base}/incident/{incident_id}"
    return forward_request_to_external(url, 'DELETE')

@incident_bp.route('/incident/<string:incident_id>/logs', methods=['POST'])
@jwt_required()
def create_incident_log(incident_id):
    url = f"{external_url_base}/incident/{incident_id}/logs"
    return forward_request_to_external(url, 'POST', request.json)

@incident_bp.route('/incident/<string:incident_id>/logs', methods=['GET'])
@jwt_required()
def get_logs_for_incident(incident_id):
    url = f"{external_url_base}/incident/{incident_id}/logs"
    return forward_request_to_external(url, 'GET')

@incident_bp.route('/incident/<string:incident_id>/logs/<string:log_id>', methods=['GET'])
@jwt_required()
def get_log_by_id(incident_id, log_id):
    url = f"{external_url_base}/incident/{incident_id}/logs/{log_id}"
    return forward_request_to_external(url, 'GET')

@incident_bp.route('/incident/<string:incident_id>/logs/<string:log_id>', methods=['PUT'])
@jwt_required()
def update_log(incident_id, log_id):
    url = f"{external_url_base}/incident/{incident_id}/logs/{log_id}"
    return forward_request_to_external(url, 'PUT', request.json)

@incident_bp.route('/incident/<string:incident_id>/logs/<string:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(incident_id, log_id):
    url = f"{external_url_base}/incident/{incident_id}/logs/{log_id}"
    return forward_request_to_external(url, 'DELETE')