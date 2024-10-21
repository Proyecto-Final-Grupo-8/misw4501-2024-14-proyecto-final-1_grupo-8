from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.models import Contract
from app.services.contract_service import ContractService

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contract', methods=['POST'])
@jwt_required()
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
    
    nuevo_contract = Contract(
        description=data.get('description'), 
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        company_id=data.get('company_id')
    )

    ContractService.create_contract(nuevo_contract)
    return jsonify({"message": "contract created", "contract": nuevo_contract.id}), 201

@contract_bp.route('/contracts', methods=['GET'])
@jwt_required()
def get_all_contract():
    contract_obj = ContractService.get_all_contract()
    return jsonify([contract.serialize() for contract in contract_obj]), 200

@contract_bp.route('/contract/<int:contract_id>', methods=['GET'])
@jwt_required()
def get_contract_by_id(contract_id):
    contract_obj = ContractService.get_contract_by_id(contract_id)
    if not contract_obj:
        return jsonify({"message": "contract not found"}), 404
    return jsonify(contract_obj.serialize()), 200

@contract_bp.route('/contract/<int:contract_id>', methods=['PUT'])
@jwt_required()
def update_contract(contract_id):
    data = request.json
    contract_obj = ContractService.update_contract(contract_id, data)
    if not contract_obj:
        return jsonify({"message": "contract not found"}), 404
    return jsonify(contract_obj.serialize()), 200

@contract_bp.route('/contract/<int:contract_id>', methods=['DELETE'])
@jwt_required()
def delete_contract(contract_id):
    contract_obj = ContractService.delete_contract(contract_id)
    if not contract_obj:
        return jsonify({"message": "contract not found"}), 404
    return jsonify({"message": "contract deleted"}), 200