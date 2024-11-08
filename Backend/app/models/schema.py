import strawberry
from typing import List, Optional
from app.models import Users, Incident, IncidentLog, Contract, Company, Rates, Invoices, LogInvoices, CompanyServices
from app.extensions import db

# Definición de tipos de GraphQL

@strawberry.type
class UserType:
    id: str
    username: str
    email: str
    phone: str
    name: str
    last_name: str
    role: str

@strawberry.type
class IncidentType:
    id: str
    description: str
    created_date: str
    modified_date: str
    source: str
    #customer_id: str
    #analyst_id: str
    status: str
    logs: List['IncidentLogType']

    @strawberry.field
    def customer(self) -> UserType:
        user = db.session.query(Users).filter(Users.id == self.customer_id).first()
        return UserType(id=user.id, username=user.username, email=user.email, phone=user.phone, name=user.name, last_name=user.last_name, role=user.role)
    
    # @strawberry.field
    # def analyst(self) -> UserType:
    #     user = db.session.query(Users).filter(Users.id == self.analyst_id).first()
    #     return UserType(id=user.id, username=user.username, email=user.email, phone=user.phone, name=user.name, last_name=user.last_name, role=user.role)


@strawberry.type
class IncidentLogType:
    id: str
    details: str
    created_date: str
    incident_id: str

    @strawberry.field
    def user(self) -> UserType:
        user = db.session.query(Users).filter(Users.id == self.users_id).first()
        return UserType(id=user.id, username=user.username, email=user.email, phone=user.phone, name=user.name, last_name=user.last_name, role=user.role)

@strawberry.type
class ContractType:
    id: str
    description: str
    start_date: str
    end_date: str
    plan: str
    company_id: str

@strawberry.type
class CompanyType:
    id: str
    name: str
    created_date: str
    users: List['UserType']
    contracts: List['ContractType']

@strawberry.type
class RatesType:
    id: str
    rate: float
    rate_per_incident: float
    id_contract: str
    source: str

@strawberry.type
class InvoicesType:
    id: str
    amount: float
    id_contract: str
    company_id: str
    created_date: str

@strawberry.type
class LogInvoicesType:
    id: str
    amount: float
    id_invoice: str
    created_date: str
    quantity: int
    description: str
    source: str

@strawberry.type
class CompanyServicesType:
    id: str
    description: str
    id_company: str
    created_date: str

# Definición de las consultas en GraphQL

@strawberry.type
class Query:
    @strawberry.field 
    def users(self, id: Optional[str] = None, username: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, name: Optional[str] = None, last_name: Optional[str] = None, role: Optional[str] = None ) -> List[UserType]: 
        query = db.session.query(Users) 
        filters = { 
            "id": id, 
            "username": username, 
            "email": email, 
            "phone": phone, 
            "name": name, 
            "last_name": last_name, 
            "role": role 
            } 
        for key, value in filters.items(): 
            if value is not None: 
                query = query.filter(getattr(Users, key).like(f"%{value}%")) 
        return query.all()

    @strawberry.field
    def incidents(self,description: Optional[str] = None, created_date: Optional[str] = None, modified_date: Optional[str] = None, source: Optional[str] = None, status: Optional[str] = None ) -> List[IncidentType]:
        query = db.session.query(Incident)
        filter = {
            "description": description,
            "created_date": created_date,
            "modified_date": modified_date,
            "source": source,
            "status": status
        }
        for key, value in filter.items():
            if value:
                query = query.filter(getattr(Incident, key).like(f"%{value}%"))
        return query.all()

    @strawberry.field
    def log_invoices(self, id: Optional[str] = None, amount: Optional[float] = None, id_invoice: Optional[str] = None, created_date: Optional[str] = None, quantity: Optional[int] = None, description: Optional[str] = None, source: Optional[str] = None) -> List[LogInvoicesType]:
        query = db.session.query(LogInvoices)
        filters = {
            "id": id,
            "amount": amount,
            "id_invoice": id_invoice,
            "created_date": created_date,
            "quantity": quantity,
            "description": description,
            "source": source
        }
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(LogInvoices, key).like(f"%{value}%"))
        return query.all()

    @strawberry.field
    def contracts(self, id: Optional[str] = None, description: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, plan: Optional[str] = None, company_id: Optional[str] = None) -> List[ContractType]:
        query = db.session.query(Contract)
        filters = {
            "id": id,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "plan": plan,
            "company_id": company_id
        }
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(Contract, key).like(f"%{value}%"))
        return query.all()

    @strawberry.field
    def companies(self, id: Optional[str] = None, name: Optional[str] = None, created_date: Optional[str] = None) -> List[CompanyType]:
        query = db.session.query(Company)
        filters = {
            "id": id,
            "name": name,
            "created_date": created_date
        }
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(Company, key).like(f"%{value}%"))
        return query.all()

    @strawberry.field
    def rates(self, id: Optional[str] = None, rate: Optional[float] = None, rate_per_incident: Optional[float] = None, id_contract: Optional[str] = None, source: Optional[str] = None) -> List[RatesType]:
        query = db.session.query(Rates)
        filters = {
            "id": id,
            "rate": rate,
            "rate_per_incident": rate_per_incident,
            "id_contract": id_contract,
            "source": source
        }
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(Rates, key).like(f"%{value}%"))
        return query.all()

    @strawberry.field
    def invoices(self, id: Optional[str] = None, amount: Optional[float] = None, id_contract: Optional[str] = None, company_id: Optional[str] = None, created_date: Optional[str] = None) -> List[InvoicesType]:
        query = db.session.query(Invoices)
        filters = {
            "id": id,
            "amount": amount,
            "id_contract": id_contract,
            "company_id": company_id,
            "created_date": created_date
        }

    @strawberry.field
    def log_invoices(self, id: Optional[str] = None, amount: Optional[float] = None, id_invoice: Optional[str] = None, created_date: Optional[str] = None, quantity: Optional[int] = None, description: Optional[str] = None, source: Optional[str] = None) -> List[LogInvoicesType]:
        query = db.session.query(LogInvoices)
        filters = {
            "id": id,
            "amount": amount,
            "id_invoice": id_invoice,
            "created_date": created_date,
            "quantity": quantity,
            "description": description,
            "source": source
        }
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(LogInvoices, key).like(f"%{value}%"))
        return query.all()

    @strawberry.field
    def company_services(self, id: Optional[str] = None, description: Optional[str] = None, id_company: Optional[str] = None, created_date: Optional[str] = None) -> List[CompanyServicesType]:
        query = db.session.query(CompanyServices)
        filters = {
            "id": id,
            "description": description,
            "id_company": id_company,
            "created_date": created_date
        }
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(CompanyServices, key).like(f"%{value}%"))
        return query.all()

# Definir el esquema de GraphQL
schema = strawberry.Schema(query=Query)
