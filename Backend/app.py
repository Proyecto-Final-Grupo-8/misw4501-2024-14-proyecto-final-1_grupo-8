from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from Modelos.modelo import RegistroIncidentesSchema, db, RegistroLlamadas
from datetime import datetime
from dotenv import load_dotenv
import os


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

class Estado(Resource):
    def get(self):
        return {"status": "OK"}, 200

api.add_resource(Estado, '/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=5000)

