from app.models.models import Company
from app.extensions import db

class CompanyService:
    @staticmethod
    def get_all_companies():        
        return Company.query.all()