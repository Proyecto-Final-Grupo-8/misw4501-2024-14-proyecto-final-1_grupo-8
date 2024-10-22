from app import db
from sqlalchemy.sql import func
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo de Users
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024))
    company_id = db.Column(db.String(36), db.ForeignKey('company.id'), nullable=False)
    
    # Rol del users: customer, analyst, o company
    role = db.Column(db.String(20), nullable=False)
    
    # Relación con el modelo de incident (customer y analyst)
    incident_customer = db.relationship('Incident', backref='customer', lazy=True, foreign_keys='Incident.customer_id')
    incident_analyst = db.relationship('Incident', backref='analyst', lazy=True, foreign_keys='Incident.analyst_id')
    incident_log = db.relationship('IncidentLog', backref='users', lazy=True, foreign_keys='IncidentLog.users_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Incident
class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())
    modified_date = db.Column(db.DateTime, default=db.func.now())
    source = db.Column(db.String(20), nullable=True)
    customer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    analyst_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    status = db.Column(db.String(20), nullable=False, default='Abierto')

    # Relaciones
    logs = db.relationship('IncidentLog', backref='incident', lazy=True, cascade="all, delete")

    def asignar_analyst(self, analyst):
        self.analyst_id = analyst.id
        self.status = 'En Proceso'

    def cerrar_incident(self):
        self.status = 'Cerrado'

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_date': self.created_date,
            'source': self.source,
            'customer': self.customer.username,  # Accedemos al customer correctamente
            'analyst': self.analyst.username if self.analyst else None,  # Solo mostramos si hay analyst
            'status': self.status,
            'logs': [log.serialize() for log in self.logs] 
        }

# Modelo de Log de Incident
class IncidentLog(db.Model):
    __tablename__ = 'log_incident'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    details = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())
    users_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    incident_id = db.Column(db.String(36), db.ForeignKey('incident.id'), nullable=False)  # Corregido a String(36)

    def serialize(self):
        return {
            'id': self.id,
            'details': self.details,
            'created_date': self.created_date,
            'user': self.users.username  # Cambiado 'users' a 'user'
        }

# Modelo de Contract
class Contract(db.Model):
    __tablename__ = 'contract'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    company_id = db.Column(db.String(36), db.ForeignKey('company.id'), nullable=False)

    company = db.relationship('Company', backref='contracts')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'company': self.company.name
        }

# Modelo de Company
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('Users', backref='company', lazy=True)
    created_date = db.Column(db.DateTime, default=db.func.now())

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

# Modelo de Rates
class Rates(db.Model):
    __tablename__ = 'rates'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rate = db.Column(db.Float, nullable=False)
    rate_per_incident = db.Column(db.Float, nullable=False)
    id_contract = db.Column(db.String(36), db.ForeignKey('contract.id'), nullable=False)
    source = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'rate': self.rate,
            'rate_per_incident': self.rate_per_incident,
            'contract': self.id_contract,
            'source': self.source
        }