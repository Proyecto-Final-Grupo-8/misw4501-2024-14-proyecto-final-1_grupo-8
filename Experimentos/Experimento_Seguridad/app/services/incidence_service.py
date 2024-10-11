from flask import Blueprint, request, jsonify
from app import db
from app.models import Incidence
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

incidence_bp = Blueprint('incidence_bp', __name__)

def create_incidence(user_id, data):
    new_incidence = Incidence(
        user_id=user_id,
        creation_date=data.get('creation_date'),
        description=data.get('description')
    )
    db.session.add(new_incidence)
    db.session.commit()
    return new_incidence

def get_incidences(user_id):
    print(f"{user_id =}")
    incidences = Incidence.query.filter_by(user_id=user_id)
    return incidences

def get_incidence(user_id,incidence_id):
    incidence = Incidence.query.get_or_404(incidence_id)
    return incidence

def update_incidence(user_id,incidence_id, data):
    incidence = Incidence.query.get_or_404(incidence_id)
    incidence.creation_date = datetime.datetime.now()
    incidence.description = data.get('description', incidence.description)
    db.session.commit()
    return incidence

def delete_incidence(user_id,incidence_id):
    incidence = Incidence.query.get_or_404(incidence_id)
    db.session.delete(incidence)
    db.session.commit()
    return