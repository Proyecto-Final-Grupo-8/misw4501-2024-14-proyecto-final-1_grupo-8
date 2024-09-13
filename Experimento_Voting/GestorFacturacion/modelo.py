from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class RegistroFacturacion(db.Model):
    __tablename__ = 'registro_facturacion'  # Nombre de la tabla
    id = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.String(100), unique=True, nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    def __str__(self) -> str:
        return f'<RegistroFacturacion {self.id_factura}>'


class RegistroFacturacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegistroFacturacion
        load_instance = True
