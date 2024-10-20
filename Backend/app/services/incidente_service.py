from app.models.models import Incidente, IncidenteLog
from app.extensions import db
from datetime import datetime

class IncidenteService:
    @staticmethod
    def create_incidente(nuevo_incidente):
        nuevo_incidente.created_at = datetime.utcnow() 
        db.session.add(nuevo_incidente)
        db.session.commit()
        return nuevo_incidente

    @staticmethod
    def get_all_incidente(user_id,user_role):
        if user_role == 'cliente':
            return Incidente.query.filter_by(cliente_id=user_id).all()
        elif user_role == 'analista':
            return Incidente.query.all()

    @staticmethod
    def get_incidente_by_id(user_id,user_role,incidente_id):
        if user_role == 'cliente':
            return Incidente.query.filter_by(cliente_id=user_id, id=incidente_id).first()
        elif user_role == 'analista':
            return Incidente.query.get_or_404(incidente_id)
        
    @staticmethod
    def update_incidente(incidente_id, data):

        incidente = Incidente.query.get(incidente_id)        
        if not incidente:
            return None        
        incidente.estado = data.get('estado', incidente.estado)
        incidente.fecha_modificacion = datetime.utcnow()
        db.session.commit()
        return incidente

    @staticmethod
    def create_incidente_log(nuevo_log):
        nuevo_log.created_at = datetime.utcnow()
        db.session.add(nuevo_log)
        db.session.commit()
        return nuevo_log

    @staticmethod
    def get_logs_for_incidente(incidente_id):
        return IncidenteLog.query.filter_by(incidente_id=incidente_id).all()
