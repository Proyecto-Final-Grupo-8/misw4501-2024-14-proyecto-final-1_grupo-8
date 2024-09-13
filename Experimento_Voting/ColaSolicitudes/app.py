from flask import Flask, jsonify
from flask_restful import Resource, Api
from Experimento_Voting.ColaSolicitudes.Celery.tasks import solicitudFactura as solicitudFacturaTask, estadoMicroservicio as estadoMicroservicioTask

app = Flask(__name__)
api = Api(app)

class solicitudFactura(Resource):
    def get(self, id_factura):
        if not id_factura:
            return {"error": "id_factura es necesario"}, 400
        
        # Enviar la tarea a Celery en segundo plano
        task = solicitudFacturaTask.delay(id_factura)
        
        return jsonify({"message": "Solicitud enviada", "task_id": task.id})


class estadoMicroservicio(Resource):
    def get(self):
        # Enviar la tarea a Celery en segundo plano para verificar el estado del microservicio
        task = estadoMicroservicioTask.delay()
        return jsonify({"message": "Estado del microservicio solicitado", "task_id": task.id}), 202


api.add_resource(estadoMicroservicio, '/')
api.add_resource(solicitudFactura, '/SolicitudFactura/<string:id_factura>')

if __name__ == '__main__':
    app.run(debug=True, port=5004)
