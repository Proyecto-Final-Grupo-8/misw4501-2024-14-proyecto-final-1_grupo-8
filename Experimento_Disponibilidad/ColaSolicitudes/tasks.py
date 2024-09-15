import os
from dotenv import load_dotenv
from datetime import datetime
from celery import Celery
import requests

load_dotenv()
redis_host = os.getenv('Redis_HOST')
MC1_host = os.getenv('MC1_HOST')
MC2_host = os.getenv('MC2_HOST')
MC3_host = os.getenv('MC3_HOST')

MC1_port = os.getenv('MC1_PORT')
MC2_port = os.getenv('MC2_PORT')
MC3_port = os.getenv('MC3_PORT')


app = Celery('cola_solicitudes', broker=f'redis://{redis_host}:6379/0', backend=f'redis://{redis_host}:6379/0')

@app.task(name='cola_solicitudes.solicitudFactura')
def solicitudFactura(id_factura, body_data):

    try:
        Response_GF1 = requests.post(f'http://{MC1_host}:{MC1_port}/{id_factura}', json=body_data)
        Response_GF1.raise_for_status()
        Response_GF1 = Response_GF1.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en el microservicio 1: {str(e)}"}

    try:
        Response_GF2 = requests.post(f'http://{MC2_host}:{MC2_port}/{id_factura}', json=body_data)
        Response_GF2.raise_for_status()
        Response_GF2 = Response_GF2.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en el microservicio 2: {str(e)}"}

    try:
        Response_GF3 = requests.post(f'http://{MC3_host}:{MC3_port}/{id_factura}', json=body_data)
        Response_GF3.raise_for_status()
        Response_GF3 = Response_GF3.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en el microservicio 3: {str(e)}"}
    

    if Response_GF1 == Response_GF2 == Response_GF3:
        statuses = ["Microservicio 1: Normal", "Microservicio 2: Normal", "Microservicio 3: Normal"]
        Response = Response_GF1
    elif Response_GF1 != Response_GF2 and Response_GF1 != Response_GF3 and Response_GF2 == Response_GF3:
        statuses = ["Microservicio 1: Fallando", "Microservicio 2: Normal", "Microservicio 3: Normal"]
        Response = Response_GF2
    elif Response_GF1 != Response_GF2 and Response_GF1 == Response_GF3 and Response_GF2 != Response_GF3:
        statuses = ["Microservicio 1: Normal", "Microservicio 2: Fallando", "Microservicio 3: Normal"]
        Response = Response_GF1
    elif Response_GF1 == Response_GF2 and Response_GF1 != Response_GF3 and Response_GF2 != Response_GF3:
        statuses = ["Microservicio 1: Normal", "Microservicio 2: Normal", "Microservicio 3: Fallando"]
        Response = Response_GF1
    else:
        statuses = ["Microservicio 1: Fallando", "Microservicio 2: Fallando", "Microservicio 3: Fallando"]
        Response = {"message": "El sistema de Facturacion fallo Completamente", "statuses": statuses}
    
    return {"message": "Solicitud de factura procesada", "response": Response, "statuses": statuses}




#    responses = [Response_GF1, Response_GF2, Response_GF3]
#    statuses = ["Fallando" if responses.count(resp) < 2 else "Normal" for resp in responses]

#    for i, response in enumerate([Response_GF1, Response_GF2, Response_GF3]):
#        response['statusMicroservicio'] = statuses[i]

#    if all(status == "Normal" for status in statuses):
#        return Response_GF1
#    else:
#        return {"message": "Inconsistencia entre microservicios", "statuses": statuses}


@app.task(name='cola_solicitudes.estadoMicroservicio')
def estadoMicroservicio():
    return f'ColaSolicitudes Funcionando - {datetime.now()}'
