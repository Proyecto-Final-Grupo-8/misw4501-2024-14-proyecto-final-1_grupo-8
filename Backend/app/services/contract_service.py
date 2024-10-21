from app.models.models import Contract
from app.extensions import db

class ContractService:
    @staticmethod
    def create_contract(nuevo_contract):
        db.session.add(nuevo_contract)
        db.session.commit()
        return nuevo_contract
    
    @staticmethod
    def get_contract_by_id(contract_id):
        return Contract.query.get_or_404(contract_id)
    
    @staticmethod
    def get_all_contract():
        return Contract.query.all()
    
    @staticmethod
    def update_contract(contract_id, contract_data):
        contract = Contract.query.get(contract_id)
        if not contract:
            return None
        contract.description = contract_data.get('description', contract.description)
        contract.start_date = contract_data.get('start_date', contract.start_date)
        contract.end_date = contract_data.get('end_date', contract.end_date)
        contract.company_id = contract_data.get('company_id', contract.company_id)
        db.session.commit()
        return contract

    @staticmethod
    def delete_contract(contract_id):
        contract = Contract.query.get(contract_id)
        if not contract:
            return None
        db.session.delete(contract)
        db.session.commit()
        return contract