
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from faker import Faker
from Modelos.modelo import RegistroIncidentesSchema, db, RegistroIncidentes
from datetime import datetime
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde un archivo .env específico
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), override=True)


IdentificadorMC = os.getenv('IdentificadorMC')

db_user = 'postgres'
db_password = 'postgres'
db_host = 'database-1.cnyu44uss058.us-east-1.rds.amazonaws.com'
db_port = '5432'
db_name = 'postgres'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)
fake = Faker()


class CrearIncidente(Resource):

    def post(self):
        data = request.get_json()
        
        # Validar los campos obligatorios
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')

        if not titulo or not descripcion:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Crear el registro en la base de datos
        nuevo_incidente = RegistroIncidentes(
            titulo=titulo,
            descripcion=descripcion,
            fecha_apertura=datetime.now(),
            fecha_cierre=None,
            estado="Abierto"
        )

        try:
            db.session.add(nuevo_incidente)
            db.session.commit()
            return {"status": "Incidente creado exitosamente"}, 201

        except Exception as e:
            db.session.rollback()
            return {"status": "Fallo", "error": str(e)}, 500



class Estado(Resource):
    def get(self):
        return {"status": "OK"}, 200

api.add_resource(CrearIncidente, '/crear-incidente')
api.add_resource(Estado, '/')


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5000)

