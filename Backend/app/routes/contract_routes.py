from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.models import Contract
from app.services.contract_service import ContractService

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contract', methods=['POST'])
def create_contract():
    data = request.json

    if not data.get('description'):
        return jsonify({"message": "description is required"}), 400
    
    if not data.get('start_date'):
        return jsonify({"message": "start_date is required"}), 400
    
    if not data.get('end_date'):
        return jsonify({"message": "end_date is required"}), 400

    if not data.get('company_id'):
        return jsonify({"message": "company_id is required"}), 400
    
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
 
    nuevo_contract = Contract(
        description=data.get('description'), 
        start_date=start_date,
        end_date=end_date,
        company_id=data.get('company_id'),
        plan=data.get('plan')
    )

    ContractService.create_contract(nuevo_contract)
    return jsonify({"message": "contract created", "contract": nuevo_contract.id}), 201

@contract_bp.route('/contracts', methods=['GET'])
def get_all_contract():
    contract_obj = ContractService.get_all_contract()
    return jsonify([contract.serialize() for contract in contract_obj]), 200

@contract_bp.route('/contract/<string:contract_id>', methods=['GET'])
def get_contract_by_id(contract_id):
    contract_obj = ContractService.get_contract_by_id(contract_id)
    if not contract_obj:
        return jsonify({"message": "contract not found"}), 404
    return jsonify(contract_obj.serialize()), 200

@contract_bp.route('/contract/<string:contract_id>', methods=['PUT'])
def update_contract(contract_id):
    data = request.json

    if data.get('start_date'):
        data['start_date'] = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    
    if data.get('end_date'):
        data['end_date'] = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()


    contract_obj = ContractService.update_contract(contract_id, data)
    if not contract_obj:
        return jsonify({"message": "contract not found"}), 404
    return jsonify({"message":"contract updated","contract":contract_obj.serialize()}), 200

@contract_bp.route('/contract/<string:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    contract_obj = ContractService.delete_contract(contract_id)
    if not contract_obj:
        return jsonify({"message": "contract not found"}), 404
    return jsonify({"message": "contract deleted"}), 200