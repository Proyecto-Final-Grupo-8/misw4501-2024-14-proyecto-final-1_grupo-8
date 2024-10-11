import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from faker import Faker
from Modelos.modelos import RegistroFacturacionSchema, db, RegistroFacturacion

load_dotenv()

IdentificadorMC = os.getenv('IdentificadorMC')

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)
fake = Faker()


class BusquedaFactura(Resource):

    def post(self, id):
        data = request.get_json()
        comportamiento = data.get('Comportamiento', None)

        if f'GestorFacturacion{IdentificadorMC}' in comportamiento:
            idBusqueda = fake.random_int(min=1, max=100)
        else:    
            idBusqueda = id

        registro = RegistroFacturacion.query.filter_by(id=idBusqueda).first()
        if registro:
            registro_schema = RegistroFacturacionSchema()
            return jsonify(registro_schema.dump(registro))
        return jsonify({'message': 'Factura no encontrada'}), 404

class Estado(Resource):
    def get(self):
        return {'status': f'GestorFacturacion_{IdentificadorMC} en funcionamiento'}


api.add_resource(BusquedaFactura, '/<int:id>')
api.add_resource(Estado, '/')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(f'host: {db_host}')
    print(f'port: {db_port}')
    print(f'user: {db_user}')
    print(f'password: {db_password}')
    print(f'db_name: {db_name}')
    print(f'IdentificadorMC: {IdentificadorMC}')
    app.run(debug=True)
    
