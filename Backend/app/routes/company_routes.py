# app/routes/company_routes.py

from flask import Blueprint, jsonify, request
from app.models.models import Company
from app import db
from app.services.users_service import create_contrac_and_company

company_bp = Blueprint('company_bp', __name__)

@company_bp.route('/register', methods=['POST'])
def register_company():
    data = request.get_json()
    name = data.get('name')
    contrac_id = data.get('contrac_id')  # Suponemos que el contrac ya está creado

    if Company.query.filter_by(name=name).first():
        return {'message': 'company already exists'}, 400

    new_company = Company(name=name, contrac_id=contrac_id)
    db.session.add(new_company)
    db.session.commit()

    return {'message': 'company created successfully'}, 201

@company_bp.route('/create_ contract', methods=['POST'])
def create_contrac():
    data = request.get_json()
    return create_contrac_and_company(data)

@company_bp.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([company.serialize() for company in companies])