from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from strawberry.flask.views import GraphQLView
from app.models.schema import schema

graphql_bp = Blueprint('graphql_bp', __name__)

# Agrega el endpoint de GraphQL al blueprint
graphql_bp.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema)
    #view_func=jwt_required()(GraphQLView.as_view("graphql_view", schema=schema))
)

@graphql_bp.route('/graphql-query', methods=['POST'])
@jwt_required()  
def graphql_query():
    # Extrae la consulta GraphQL del cuerpo de la solicitud
    data = request.get_json()
    query = data.get("query")
    
    # Ejecuta la consulta GraphQL usando el esquema
    result = schema.execute_sync(query)
    
    # Verifica si hay errores en la ejecución de la consulta
    if result.errors:
        return jsonify({"errors": [str(error) for error in result.errors]}), 400
    
    # Devuelve los datos en un formato personalizado
    return jsonify({"message": "Consulta ejecutada con éxito", "data": result.data}), 200
