from app.models.models import Incident, IncidentLog
from app.extensions import db
from datetime import datetime

class IncidentService:
    @staticmethod
    def create_incident(nuevo_incident):
        nuevo_incident.created_at = datetime.utcnow() 
        db.session.add(nuevo_incident)
        db.session.commit()
        return nuevo_incident

    @staticmethod
    def get_all_incident(user_id,user_role):
        if user_role == 'customer':
            return Incident.query.filter_by(customer_id=user_id).all()
        elif user_role == 'analyst' or user_role == 'admin':
            return Incident.query.all()

    @staticmethod
    def get_incident_by_id(user_id,user_role,incident_id):
        if user_role == 'customer':
            return Incident.query.filter_by(customer_id=user_id, id=incident_id).first()
        elif user_role == 'analyst' or user_role == 'admin':
            return Incident.query.get_or_404(incident_id)
        
    @staticmethod
    def update_incident(user_rol,incident_id, data):
        if user_rol == 'analyst':
            incident = Incident.query.get(incident_id)        
            if not incident:
                return None        
            incident.status = data.get('status', incident.status)
            incident.modified_date = datetime.utcnow()
            db.session.commit()
            return incident
        
        if user_rol == 'admin':
            incident = Incident.query.get(incident_id)
            if not incident:
                return None
            incident.description = data.get('description', incident.description)
            incident.customer_id = data.get('customer_id', incident.customer_id)
            incident.source = data.get('source', incident.source)
            incident.analyst_id = data.get('analyst_id', incident.analyst_id)
            incident.status = data.get('status', incident.status)
            db.session.commit()
            return None

    @staticmethod
    def create_incident_log(nuevo_log):
        nuevo_log.created_at = datetime.utcnow()
        db.session.add(nuevo_log)
        db.session.commit()
        return nuevo_log

    @staticmethod
    def get_logs_for_incident(incident_id):
        return IncidentLog.query.filter_by(incident_id=incident_id).all()
