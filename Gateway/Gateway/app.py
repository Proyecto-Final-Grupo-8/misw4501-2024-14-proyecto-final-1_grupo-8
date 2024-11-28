from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Base URLs de los microservicios
BACKEND_API_BASE = os.getenv("BACKEND_API_BASE", "https://backend-781163639586.us-central1.run.app/api")
BACKEND_EMAILS_BASE = os.getenv("BACKEND_EMAILS_BASE", "https://backend-emails-781163639586.us-central1.run.app")

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    """
    Redirige las solicitudes al microservicio adecuado.
    """
    if path.startswith("emails"):
        base_url = BACKEND_EMAILS_BASE
        target_url = f"{base_url}/{path[7:]}"  # Elimina "emails/" del inicio del path
    else:
        base_url = BACKEND_API_BASE
        target_url = f"{base_url}/{path}"

    # Obtener datos y encabezados de la solicitud
    data = request.get_json(silent=True) if request.method in ['POST', 'PUT'] else None
    headers = {key: value for key, value in request.headers if key != 'Host'}

    try:
        # Reenviar la solicitud al servicio correspondiente
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            json=data
        )
        # Retornar la respuesta del microservicio al cliente
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def health_check():
    """
    Endpoint de salud para verificar que el API Gateway está funcionando.
    """
    return jsonify({"status": "API Gateway is running"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
