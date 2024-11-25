import strawberry
from typing import List, Optional
from sqlalchemy.orm import joinedload
from app.models import Users, Incident, IncidentLog, Contract, Company, Rates, Invoices, LogInvoices, CompanyServices
from app.extensions import db

# Función genérica para aplicar filtros dinámicos
def apply_filters(query, model, filters: dict):
    for key, value in filters.items():
        if value is not None:
            query = query.filter(getattr(model, key) == value)
    return query

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
    status: str
    logs: List['IncidentLogType']

    @strawberry.field
    def customer(self) -> UserType:
        user = db.session.query(Users).filter(Users.id == self.customer_id).first()
        return UserType(id=user.id, username=user.username, email=user.email, phone=user.phone, name=user.name, last_name=user.last_name, role=user.role)

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
    def users(self, id: Optional[str] = None, username: Optional[str] = None, email: Optional[str] = None, 
              phone: Optional[str] = None, name: Optional[str] = None, last_name: Optional[str] = None, 
              role: Optional[str] = None) -> List[UserType]:
        filters = {
            "id": id,
            "username": username,
            "email": email,
            "phone": phone,
            "name": name,
            "last_name": last_name,
            "role": role
        }
        query = db.session.query(Users)
        query = apply_filters(query, Users, filters)
        return query.all()

    @strawberry.field
    def incidents(self, 
                  description: Optional[str] = None, 
                  created_date: Optional[str] = None, 
                  modified_date: Optional[str] = None, 
                  source: Optional[str] = None, 
                  status: Optional[str] = None, 
                  customer_id: Optional[str] = None, 
                  customer_username: Optional[str] = None, 
                  customer_email: Optional[str] = None, 
                  customer_name: Optional[str] = None,
                  incident_logs_id: Optional[str] = None,
                  incident_logs_details: Optional[str] = None,
                  incident_logs_created_date: Optional[str] = None                  
                  ) -> List[IncidentType]:
        # Filtros para la tabla Incident
        filters = {
            "description": description,
            "created_date": created_date,
            "modified_date": modified_date,
            "source": source,
            "status": status
        }
        query = db.session.query(Incident)

        # Aplicar filtros a Incident
        query = apply_filters(query, Incident, filters)

        # Filtros para la tabla relacionada Users (customer)
        if any([customer_id, customer_username, customer_email, customer_name]):
            query = query.join(Users, Users.id == Incident.customer_id)
            customer_filters = {
                "id": customer_id,
                "username": customer_username,
                "email": customer_email,
                "name": customer_name
            }
            query = apply_filters(query, Users, customer_filters)        

        # Filtros para la tabla relacionada IncidentLog
        if any([incident_logs_id, incident_logs_details, incident_logs_created_date]):
            query = query.join(IncidentLog, IncidentLog.incident_id == Incident.id)
            incident_log_filters = {
                "id": incident_logs_id,
                "details": incident_logs_details,
                "created_date": incident_logs_created_date
            }
            query = apply_filters(query, IncidentLog, incident_log_filters)

        return query.all()
    

    @strawberry.field
    def incident_logs(self, 
                      id: Optional[str] = None, 
                      details: Optional[str] = None, 
                      created_date: Optional[str] = None, 
                      incident_id: Optional[str] = None, 
                      user_id: Optional[str] = None, 
                      user_username: Optional[str] = None, 
                      user_email: Optional[str] = None, 
                      user_name: Optional[str] = None) -> List[IncidentLogType]:
        # Filtros para IncidentLog
        filters = {
            "id": id,
            "details": details,
            "created_date": created_date,
            "incident_id": incident_id
        }
        query = db.session.query(IncidentLog)
        query = apply_filters(query, IncidentLog, filters)

        # Filtros para la tabla relacionada Users (user en logs)
        if any([user_id, user_username, user_email, user_name]):
            query = query.join(Users, Users.id == IncidentLog.users_id)
            user_filters = {
                "id": user_id,
                "username": user_username,
                "email": user_email,
                "name": user_name
            }
            query = apply_filters(query, Users, user_filters)
        
        return query.all()

    @strawberry.field
    def contracts(self, id: Optional[str] = None, description: Optional[str] = None, start_date: Optional[str] = None, 
                  end_date: Optional[str] = None, plan: Optional[str] = None, company_id: Optional[str] = None) -> List[ContractType]:
        filters = {
            "id": id,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "plan": plan,
            "company_id": company_id
        }
        query = db.session.query(Contract)
        query = apply_filters(query, Contract, filters)
        return query.all()

    @strawberry.field
    def companies(self, id: Optional[str] = None, name: Optional[str] = None, created_date: Optional[str] = None) -> List[CompanyType]:
        filters = {
            "id": id,
            "name": name,
            "created_date": created_date
        }
        query = db.session.query(Company)
        query = apply_filters(query, Company, filters)
        return query.all()

    @strawberry.field
    def rates(self, id: Optional[str] = None, rate: Optional[float] = None, rate_per_incident: Optional[float] = None, 
              id_contract: Optional[str] = None, source: Optional[str] = None) -> List[RatesType]:
        filters = {
            "id": id,
            "rate": rate,
            "rate_per_incident": rate_per_incident,
            "id_contract": id_contract,
            "source": source
        }
        query = db.session.query(Rates)
        query = apply_filters(query, Rates, filters)
        return query.all()

    @strawberry.field
    def invoices(self, id: Optional[str] = None, amount: Optional[float] = None, id_contract: Optional[str] = None, 
                 company_id: Optional[str] = None, created_date: Optional[str] = None) -> List[InvoicesType]:
        filters = {
            "id": id,
            "amount": amount,
            "id_contract": id_contract,
            "company_id": company_id,
            "created_date": created_date
        }
        query = db.session.query(Invoices)
        query = apply_filters(query, Invoices, filters)
        return query.all()

    @strawberry.field
    def company_services(self, id: Optional[str] = None, description: Optional[str] = None, 
                         id_company: Optional[str] = None, created_date: Optional[str] = None) -> List[CompanyServicesType]:
        filters = {
            "id": id,
            "description": description,
            "id_company": id_company,
            "created_date": created_date
        }
        query = db.session.query(CompanyServices)
        query = apply_filters(query, CompanyServices, filters)
        return query.all()

# Definir el esquema de GraphQL
schema = strawberry.Schema(query=Query)
