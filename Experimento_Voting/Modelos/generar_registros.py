from faker import Faker
from flask import Flask

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Modelos.modelos import db, RegistroFacturacion

fake = Faker()

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

if __name__ == '__main__':
    app = Flask(__name__)
    
    db_user = 'postgres'
    db_password = 'postgres'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'postgres'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  
        registros_aleatorios = crear_registros_aleatorios(100)
        insertar_registros_en_db(registros_aleatorios)
