from app.models.models import incidente, incidenteLog
from app.extensions import db
from datetime import datetime

class incidenteervice:
    @staticmethod
    def create_incidente(data):
        incidente = incidente(
            title=data.get('title'),
            description=data.get('description'),
            created_by=data.get('created_by'),
            created_at=datetime.utcnow()
        )
        db.session.add(incidente)
        db.session.commit()
        return incidente

    @staticmethod
    def get_all_incidente():
        return incidente.query.all()

    @staticmethod
    def get_incidente_by_id(incidente_id):
        return incidente.query.get_or_404(incidente_id)

    @staticmethod
    def create_incidente_log(incidente_id, data):
        incidente_log = incidenteLog(
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
        return incidenteLog.query.filter_by(incidente_id=incidente_id).all()
