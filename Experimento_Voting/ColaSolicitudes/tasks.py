from datetime import datetime
from celery import Celery
import requests

app = Celery('cola_solicitudes', broker='redis://localhost:6379/0')

@app.task
def solicitudFactura(id_factura):
    try:
        Response_GF1 = requests.get(f'http://localhost:5001/{id_factura}')
        Response_GF1.raise_for_status()
        Response_GF1 = Response_GF1.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en el microservicio 1: {str(e)}"}

    try:
        Response_GF2 = requests.get(f'http://localhost:5002/{id_factura}')
        Response_GF2.raise_for_status()
        Response_GF2 = Response_GF2.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en el microservicio 2: {str(e)}"}

    try:
        Response_GF3 = requests.get(f'http://localhost:5003/{id_factura}')
        Response_GF3.raise_for_status()
        Response_GF3 = Response_GF3.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en el microservicio 3: {str(e)}"}

    responses = [Response_GF1, Response_GF2, Response_GF3]
    statuses = ["Fallando" if responses.count(resp) < 2 else "Normal" for resp in responses]

    for i, response in enumerate([Response_GF1, Response_GF2, Response_GF3]):
        response['statusMicroservicio'] = statuses[i]

    if all(status == "Normal" for status in statuses):
        return Response_GF1
    else:
        return {"message": "Inconsistencia entre microservicios", "statuses": statuses}


@app.task
def estadoMicroservicio():
    return f'ColaSolicitudes Funcionando - {datetime.now()}'
