import uuid
from app import db

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