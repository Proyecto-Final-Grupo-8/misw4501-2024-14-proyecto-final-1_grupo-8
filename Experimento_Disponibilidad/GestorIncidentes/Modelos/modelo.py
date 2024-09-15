from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class RegistroIncidentes(db.Model):
    __tablename__ = 'registro_incidetes' 
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    fecha_apertura = db.Column(db.DateTime, nullable=False)  # Cambié a fecha_apertura
    fecha_cierre = db.Column(db.DateTime, nullable=True)    # Cambié a fecha_cierre
    estado = db.Column(db.String(100), nullable=False)
    
    def __str__(self) -> str:
        return f'<RegistroIncidentes {self.id}>'

    def __init__(self, titulo, descripcion, fecha_apertura, fecha_cierre, estado):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_apertura = fecha_apertura
        self.fecha_cierre = fecha_cierre
        self.estado = estado

class RegistroIncidentesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegistroIncidentes
        load_instance = True
