from app.models.models import Company
from app.extensions import db

class CompanyService:
    @staticmethod
    def create_company(nuevo_company):
        db.session.add(nuevo_company)
        db.session.commit()
        return nuevo_company
    
    @staticmethod
    def get_company_by_id(company_id):
        return Company.query.get_or_404(company_id)
    
    @staticmethod
    def get_all_company():
        return Company.query.all()
    
    @staticmethod
    def update_company(company_id, company_data):
        company = Company.query.get(company_id)
        if not company:
            return None
        company.name = company_data.get('name', company.name)        
        db.session.commit()
        return company
    
    @staticmethod
    def delete_company(company_id):
        company = Company.query.get(company_id)
        if not company:
            return None
        db.session.delete(company)
        db.session.commit()
        return company