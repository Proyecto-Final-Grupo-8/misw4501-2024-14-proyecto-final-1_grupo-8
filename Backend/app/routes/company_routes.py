from flask import Blueprint, jsonify, request
from app.services.company_service import CompanyService
from app.models.models import Company
from app import db

company_bp = Blueprint('company_bp', __name__)

@company_bp.route('/company', methods=['POST'])
def create_company():
    data = request.json
    
    if not data.get('name'):
        return jsonify({"message": "name is required"}), 400
    
    name = data.get('name')


    if Company.query.filter_by(name=name).first():
        return {'message': 'company already exists'}, 400

    new_company = Company(name=name)
    db.session.add(new_company)
    db.session.commit()

    return {"message": "company created", "company":new_company.id }, 201

@company_bp.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([company.serialize() for company in companies])

@company_bp.route('/company/<string:company_id>', methods=['GET'])
def get_company_by_id(company_id):
    company = Company.query.get(company_id)

    if not company:
        return {'message': 'company not found'}, 404
    
    company_obj = CompanyService.get_company_by_id(company_id)
    if not company_obj:
        return jsonify({"message": "company not found"}), 404
        
    return jsonify(company_obj.serialize()), 200

@company_bp.route('/company/<string:company_id>', methods=['PUT'])
def update_company(company_id):
    data = request.json
    company = Company.query.get(company_id)
    if not company:
        return {'message': 'company not found'}, 404
    
    if not data.get('name'):
        return jsonify({"message": "name is required"}), 400
    
    CompanyService.update_company(company_id, data)
    return jsonify({"message":"company updated","company":company.serialize()}), 200

@company_bp.route('/company/<string:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return {'message': 'company not found'}, 404
    
    CompanyService.delete_company(company_id)
    return jsonify({"message": "company deleted"}), 200