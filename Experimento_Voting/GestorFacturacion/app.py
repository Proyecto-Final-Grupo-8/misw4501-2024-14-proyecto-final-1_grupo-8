from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from faker import Faker

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Modelos.modelos import RegistroFacturacionSchema, db, RegistroFacturacion

IdentificadorMC = 1

db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'

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
    app.run(debug=True)
