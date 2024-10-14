import uuid
from app import db

class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contrato.id'), nullable=False)
    usuarios = db.relationship('User', backref='empresa', lazy=True)