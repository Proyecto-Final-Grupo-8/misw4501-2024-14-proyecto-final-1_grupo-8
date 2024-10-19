from app.models.models import Incidence, IncidenceLog
from app.extensions import db
from datetime import datetime

class IncidenceService:
    @staticmethod
    def create_incidence(data):
        incidence = Incidence(
            title=data.get('title'),
            description=data.get('description'),
            created_by=data.get('created_by'),
            created_at=datetime.utcnow()
        )
        db.session.add(incidence)
        db.session.commit()
        return incidence

    @staticmethod
    def get_all_incidences():
        return Incidence.query.all()

    @staticmethod
    def get_incidence_by_id(incidence_id):
        return Incidence.query.get_or_404(incidence_id)

    @staticmethod
    def create_incidence_log(incidence_id, data):
        incidence_log = IncidenceLog(
            incidence_id=incidence_id,
            detail=data.get('detail'),
            created_by=data.get('created_by'),
            created_at=datetime.utcnow()
        )
        db.session.add(incidence_log)
        db.session.commit()
        return incidence_log

    @staticmethod
    def get_logs_for_incidence(incidence_id):
        return IncidenceLog.query.filter_by(incidence_id=incidence_id).all()
