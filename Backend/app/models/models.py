from app import db
from sqlalchemy.sql import func
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024))
    empresa_id = db.Column(db.String(36), db.ForeignKey('empresa.id'), nullable=False)
    
    # Rol del usuario: cliente, analista, o empresa
    role = db.Column(db.String(20), nullable=False)
    
    # Relación con el modelo de incidente (cliente y analista)
    incidente_cliente = db.relationship('Incidente', backref='cliente', lazy=True, foreign_keys='Incidente.cliente_id')
    incidente_analista = db.relationship('Incidente', backref='analista', lazy=True, foreign_keys='Incidente.analista_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Incidente
class Incidente(db.Model):
    __tablename__ = 'incidente'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    # Relación con cliente y analista
    cliente_id = db.Column(db.String(36), db.ForeignKey('usuario.id'), nullable=False)
    analista_id = db.Column(db.String(36), db.ForeignKey('usuario.id'))

    # Estado del incidente
    estado = db.Column(db.String(20), nullable=False, default='Abierto')

    # Relación uno a muchos con los logs de incidente
    logs = db.relationship('IncidenteLog', backref='incidente', lazy=True, cascade="all, delete")

    def asignar_analista(self, analista):
        self.analista_id = analista.id
        self.estado = 'En Proceso'

    def cerrar_incidente(self):
        self.estado = 'Cerrado'

# Modelo de Log de Incidente
class IncidenteLog(db.Model):
    __tablename__ = 'log_incidente'
    id = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuario.id'), nullable=False)
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidente.id'), nullable=False)

# Modelo de Contrato
class Contrato(db.Model):
    __tablename__ = 'contrato'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)

# Modelo de Empresa
class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contrato.id'), nullable=False)
    usuarios = db.relationship('Usuario', backref='empresa', lazy=True)
