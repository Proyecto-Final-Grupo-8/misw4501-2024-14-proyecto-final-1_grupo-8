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
    def get_all_incidente():
        return Incidente.query.all()

    @staticmethod
    def get_incidente_by_id(incidente_id):
        return Incidente.query.get_or_404(incidente_id)

    @staticmethod
    def create_incidente_log(incidente_id, data):
        incidente_log = IncidenteLog(
            incidente_id=incidente_id,
            detail=data.get('detail'),
            created_by=data.get('created_by'),
            created_at=datetime.utcnow()
        )
        db.session.add(incidente_log)
        db.session.commit()
        return incidente_log

    @staticmethod
    def get_logs_for_incidente(incidente_id):
        return IncidenteLog.query.filter_by(incidente_id=incidente_id).all()
