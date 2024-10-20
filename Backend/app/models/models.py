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
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())
    users_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'details': self.details,
            'created_date': self.created_date,
            'users': self.users.username
        }

# Modelo de Contrac
class Contrac(db.Model):
    __tablename__ = 'contrac'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

# Modelo de Company
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    contrac_id = db.Column(db.Integer, db.ForeignKey('contrac.id'), nullable=False)
    users = db.relationship('Users', backref='company', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
