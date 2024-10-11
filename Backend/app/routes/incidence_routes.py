# from flask import Blueprint, request, jsonify
# from app import db
# from app.models import Incidence
# import uuid
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.services.incidence_service import (
#     create_incidence, 
#     get_incidence, 
#     get_incidences, 
#     update_incidence, 
#     delete_incidence)
# from app.serializers.incidence_serializaers import(
#     IncidenceSerializer
# )

# incidence_bp = Blueprint('incidence_bp', __name__)

# # Crear una nueva incidencia
# @incidence_bp.route('/incidences', methods=['POST'])
# @jwt_required()
# def create():
#     data = request.get_json()
#     current_user = get_jwt_identity()
#     incidence = create_incidence(current_user, data)
#     incidence_serializer = IncidenceSerializer()
#     serialized_incidence = incidence_serializer.dump(incidence)
#     return jsonify(serialized_incidence), 201

# # Obtener todas las incidencias
# @incidence_bp.route('/incidences', methods=['GET'])
# @jwt_required()
# def get_all():
#     current_user = get_jwt_identity()
#     result = get_incidences(current_user)
#     incidence_serializer = IncidenceSerializer()
#     response = [incidence_serializer.dump(r) for r in result]
#     return jsonify(response), 200

# # Obtener una incidencia por ID
# @incidence_bp.route('/incidences/<incidence_id>', methods=['GET'])
# @jwt_required()
# def get_detail(incidence_id):
#     current_user = get_jwt_identity()
#     incidence = get_incidence(current_user, incidence_id)
#     incidence_serializer = IncidenceSerializer()
#     serialized_incidence = incidence_serializer.dump(incidence)
#     return jsonify(serialized_incidence), 200

# # Actualizar una incidencia
# @incidence_bp.route('/incidences/<incidence_id>', methods=['PUT'])
# @jwt_required()
# def update(incidence_id):
#     data = request.get_json()
#     current_user = get_jwt_identity()
#     incidence = update_incidence(current_user,incidence_id, data)
#     incidence_serializer = IncidenceSerializer()
#     serialized_incidence = incidence_serializer.dump(incidence)
#     return jsonify(serialized_incidence), 200

# # Eliminar una incidencia
# @incidence_bp.route('/incidences/<incidence_id>', methods=['DELETE'])
# @jwt_required()
# def delete(incidence_id):
#     current_user = get_jwt_identity()
#     delete_incidence(current_user, incidence_id)
#     return jsonify({}), 204
