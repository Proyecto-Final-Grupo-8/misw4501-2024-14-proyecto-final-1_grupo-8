import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from celery import Celery
from dotenv import load_dotenv
from modelos import db, RegistroFacturacion
from faker import Faker

fake = Faker()

load_dotenv()

redis_host = os.getenv('Redis_HOST')

# Inicialización de la app Flask y configuración
app = Flask(__name__)
db_user = 'postgres'
db_password = 'postgres'
db_host = 'postgres-db'
db_port = '5432'
db_name = 'postgres'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

Celery_app = Celery('cola_solicitudes', broker=f'redis://{redis_host}:6379/0')

def crear_registros_aleatorios(cantidad=100):
    registros = []
    for _ in range(cantidad):
        registro = RegistroFacturacion(
            id_factura=fake.unique.uuid4(),
            cliente=fake.name(),
            monto=round(fake.random_number(digits=5, fix_len=False) * 1.0, 2),  
            fecha=fake.date_time_this_year()  
        )
        registros.append(registro)
    return registros

def insertar_registros_en_db(registros):
    try:
        db.session.bulk_save_objects(registros)
        db.session.commit()
        print(f'{len(registros)} registros insertados con éxito.')
    except Exception as e:
        db.session.rollback()
        print(f'Error al insertar los registros: {str(e)}')

# Inicialización de la API Flask-RESTful
api = Api(app)

class SolicitudFactura(Resource):
    def post(self, id_factura):
        if not id_factura:
            return {"error": "id_factura es necesario"}, 400
        
        body_data = request.get_json()
        if not body_data:
            return {"error": "El cuerpo de la solicitud es necesario"}, 400

        task = Celery_app.send_task('cola_solicitudes.solicitudFactura', args=[id_factura, body_data])
        
        return jsonify({"message": "Solicitud enviada", "task_id": task.id})

class EstadoMicroservicio(Resource):
    def get(self):
        return jsonify({"message": "API Funcionando"})

# Agregar recursos al API
api.add_resource(EstadoMicroservicio, '/')
api.add_resource(SolicitudFactura, '/SolicitudFactura/<string:id_factura>')

if __name__ == '__main__':
    with app.app_context():
        try:
            # Verificación de conexión a la base de datos
            connection = db.engine.connect()
            print("Conexión exitosa a la base de datos.")
            connection.close()
            
            # Crear las tablas e insertar los registros
            print("Creando tablas...")
            db.create_all()
            print("Tablas creadas con éxito.")
            
            print("Insertando registros aleatorios...")
            registros_aleatorios = crear_registros_aleatorios(100)
            insertar_registros_en_db(registros_aleatorios)
            print("Registros insertados con éxito.")
        except Exception as e:
            print(f"Error al conectar o inicializar la base de datos: {str(e)}")

    # Ejecutar la aplicación
    app.run(debug=True, host="0.0.0.0", port=5000)

