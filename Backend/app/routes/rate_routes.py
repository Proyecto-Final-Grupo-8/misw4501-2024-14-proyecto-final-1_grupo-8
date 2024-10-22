from flask import Blueprint, jsonify, request
from app.services.rate_service import RateService
from app.models.models import Rates
from app import db

rate_bp = Blueprint('rate_bp', __name__)

@rate_bp.route('/rate', methods=['POST'])
def create_rate():
    data = request.json
    
    if not data.get('rate'):
        return jsonify({"message": "rate is required"}), 400
    if not data.get('rate_per_incident'):
        return jsonify({"message": "rate_per_incident is required"}), 400
    if not data.get('id_contract'):
        return jsonify({"message": "id_contract is required"}), 400
    if not data.get('source'):
        return jsonify({"message": "source is required"}), 400
    if data.get('source') not in ['web', 'app', 'telefono', 'email']:
        return jsonify({"message": "source is invalid"}), 400
    
    nuevo_rate = Rates(
        rate=data.get('rate'), 
        rate_per_incident=data.get('rate_per_incident'),
        id_contract=data.get('id_contract'),
        source=data.get('source')
    )

    RateService.create_rate(nuevo_rate)
    return jsonify({"message": "rate created", "rate": nuevo_rate.id}), 201

@rate_bp.route('/rates', methods=['GET'])
def get_all_rate():
    rate_obj = RateService.get_all_rate()
    return jsonify([rate.serialize() for rate in rate_obj]), 200

@rate_bp.route('/rate/<string:rate_id>', methods=['GET'])
def get_rate_by_id(rate_id):
    rate_obj = RateService.get_rate_by_id(rate_id)
    if not rate_obj:
        return jsonify({"message": "rate not found"}), 404
    return jsonify(rate_obj.serialize()), 200

@rate_bp.route('/rate/<string:rate_id>', methods=['PUT'])
def update_rate(rate_id):
    data = request.json
    rate_obj = RateService.update_rate(rate_id, data)
    if not rate_obj:
        return jsonify({"message": "rate not found"}), 404
    return jsonify({"message":"rate updated","rate":rate_obj.serialize()}), 200

@rate_bp.route('/rate/<string:rate_id>', methods=['DELETE'])
def delete_rate(rate_id):
    rate_obj = RateService.delete_rate(rate_id)
    if not rate_obj:
        return jsonify({"message": "rate not found"}), 404
    return jsonify({"message": "rate deleted"}), 200