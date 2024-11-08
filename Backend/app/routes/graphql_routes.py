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
    data = request.get_json()
    query = data.get("query")
    
    result = schema.execute_sync(query)
    
    if result.errors:
        return jsonify({"errors": [str(error) for error in result.errors]}), 400
    
    return jsonify({"message": "Consulta ejecutada con éxito", "data": result.data}), 200
