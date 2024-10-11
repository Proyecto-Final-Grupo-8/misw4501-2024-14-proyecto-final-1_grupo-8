import uuid
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024))
    empresa_id = db.Column(db.String(36), db.ForeignKey('empresa.id'), nullable=False)
    
    # Rol del usuario: cliente, analista, o empresa
    role = db.Column(db.String(20), nullable=False)
    
    # Relación con el modelo de incidencias (solo si es cliente o analista)
    incidencias_cliente = db.relationship('Incidencia', backref='cliente', lazy=True, foreign_keys='Incidencia.cliente_id')
    incidencias_analista = db.relationship('Incidencia', backref='analista', lazy=True, foreign_keys='Incidencia.analista_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)