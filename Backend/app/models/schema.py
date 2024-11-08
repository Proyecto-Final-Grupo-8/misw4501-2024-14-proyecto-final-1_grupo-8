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
    customer_id: str
    analyst_id: str
    status: str

@strawberry.type
class IncidentLogType:
    id: str
    details: str
    created_date: str
    users_id: str
    incident_id: str

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
    def users(self) -> List[UserType]:
        return db.session.query(Users).all()

    @strawberry.field
    def incidents(self) -> List[IncidentType]:
        return db.session.query(Incident).all()

    @strawberry.field
    def incident_logs(self) -> List[IncidentLogType]:
        return db.session.query(IncidentLog).all()

    @strawberry.field
    def contracts(self) -> List[ContractType]:
        return db.session.query(Contract).all()

    @strawberry.field
    def companies(self) -> List[CompanyType]:
        return db.session.query(Company).all()

    @strawberry.field
    def rates(self) -> List[RatesType]:
        return db.session.query(Rates).all()

    @strawberry.field
    def invoices(self) -> List[InvoicesType]:
        return db.session.query(Invoices).all()

    @strawberry.field
    def log_invoices(self) -> List[LogInvoicesType]:
        return db.session.query(LogInvoices).all()

    @strawberry.field
    def company_services(self) -> List[CompanyServicesType]:
        return db.session.query(CompanyServices).all()

# Definir el esquema de GraphQL
schema = strawberry.Schema(query=Query)