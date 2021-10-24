from flask import Blueprint, jsonify
from models.books import Books

health_check_blueprint = Blueprint('health_check_blueprint', __name__)


@health_check_blueprint.route('/health', methods=['GET'])
def health():
    try:
        Books.objects()
    except:
        return jsonify({"message": "Cannot connect to database"}), 500
    return jsonify({"message": "Healthy"})

