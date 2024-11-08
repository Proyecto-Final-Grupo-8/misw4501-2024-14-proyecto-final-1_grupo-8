import strawberry
from typing import List
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
    def users(self, id: str = None, username: str = None) -> List[UserType]:
        query = db.session.query(Users)
        if id:
            query = query.filter(Users.id.like(f"%{id}%"))
        if username:
            query = query.filter(Users.username.like(f"%{username}%"))
        return query.all()

    @strawberry.field
    def incidents(self,description: str = None) -> List[IncidentType]:
        query = db.session.query(Incident)
        if description:
            query = query.filter(Incident.description.like(f"%{description}%"))
        return query.all()

    @strawberry.field
    def incident_logs(self, details: str = None) -> List[IncidentLogType]:
        query = db.session.query(IncidentLog)
        if details:
            query = query.filter(IncidentLog.details.like(f"%{details}%"))
        return query.all()

    @strawberry.field
    def contracts(self, id: str = None, description: str = None) -> List[ContractType]:
        query = db.session.query(Contract)
        if id:
            query = query.filter(Contract.id.like(f"%{id}%"))
        if description:
            query = query.filter(Contract.description.like(f"%{description}%"))
        return query.all()

    @strawberry.field
    def companies(self, name: str = None) -> List[CompanyType]:
        query = db.session.query(Company)
        if name:
            query = query.filter(Company.name.like(f"%{name}%"))
        return query.all()

    @strawberry.field
    def rates(self, source: str = None) -> List[RatesType]:
        query = db.session.query(Rates)
        if source:
            query = query.filter(Rates.source.like(f"%{source}%"))
        return query.all()

    @strawberry.field
    def invoices(self, amount: float = None) -> List[InvoicesType]:
        query = db.session.query(Invoices)
        if amount:
            query = query.filter(Invoices.amount == amount)
        return query.all()

    @strawberry.field
    def log_invoices(self, description: str = None) -> List[LogInvoicesType]:
        query = db.session.query(LogInvoices)
        if description:
            query = query.filter(LogInvoices.description.like(f"%{description}%"))
        return query.all()

    @strawberry.field
    def company_services(self, description: str = None) -> List[CompanyServicesType]:
        query = db.session.query(CompanyServices)
        if description:
            query = query.filter(CompanyServices.description.like(f"%{description}%"))
        return query.all()

# Definir el esquema de GraphQL
schema = strawberry.Schema(query=Query)
