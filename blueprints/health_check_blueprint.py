from flask import Blueprint, jsonify
from pymongo.errors import ConnectionFailure
from MongoManager import MongoManager

health_check_blueprint = Blueprint('health_check_blueprint', __name__)


@health_check_blueprint.route('/health', methods=['GET'])
def health():
    try:
        client = MongoManager.getInstance()
        client.server_info()
    except ConnectionFailure:
        return jsonify({"message": "Cannot connect to database"}), 500
    return jsonify({"message": "Healthy"})

