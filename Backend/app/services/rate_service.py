from app.models.models import Rates
from app.extensions import db

class RateService:
    @staticmethod
    def create_rate(new_rate):
        db.session.add(new_rate)
        db.session.commit()
        return new_rate
    
    @staticmethod
    def get_rate_by_id(rate_id):
        return Rates.query.get_or_404(rate_id)
    
    @staticmethod
    def get_all_rate():
        return Rates.query.all()
    
    @staticmethod
    def update_rate(rate_id, rate_data):
        rate = db.session.get(Rates ,rate_id)
        if not rate:
            return None
        rate.rate = rate_data.get('rate', rate.rate)
        rate.rate_per_incident = rate_data.get('rate_per_incident', rate.rate_per_incident)
        rate.source = rate_data.get('source', rate.source)
        db.session.commit()
        return rate

    @staticmethod
    def delete_rate(rate_id):
        rate = db.session.get(Rates ,rate_id)
        if not rate:
            return None
        db.session.delete(rate)
        db.session.commit()
        return rate
