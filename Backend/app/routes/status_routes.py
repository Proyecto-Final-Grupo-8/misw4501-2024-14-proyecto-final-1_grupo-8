from flask import Blueprint, jsonify, request

status_bp = Blueprint('status_bp', __name__)
@status_bp.route('/', methods=['GET'])
def status():
    return jsonify({"message": "Backend running"}), 200