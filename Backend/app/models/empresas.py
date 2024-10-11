import uuid
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo Empresa
class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contrato.id'), nullable=False)
    usuarios = db.relationship('User', backref='empresa', lazy=True)

# Modelo Contrato
class Contrato(db.Model):
    __tablename__ = 'contrato'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)

# Modelo Usuario (base)


# Modelo de Incidencia
class Incidencia(db.Model):
    __tablename__ = 'incidencia'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    
    # Relación con cliente y analista
    cliente_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    analista_id = db.Column(db.String(36), db.ForeignKey('user.id'))

    # Estado de la incidencia
    estado = db.Column(db.String(20), nullable=False, default='Abierto')

    def asignar_analista(self, analista):
        self.analista_id = analista.id
        self.estado = 'En Proceso'

    def cerrar_incidencia(self):
        self.estado = 'Cerrado'