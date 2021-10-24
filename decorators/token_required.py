from functools import wraps
from flask import jsonify, request
import jwt
import os


def token_required(f):
    salt = os.environ.get("SALT")
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("authorization")
        try:
            data = jwt.decode(token, salt, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "token expired"}), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({"message": "token not valid"}), 401
        return f(*args, **kwargs)
    return decorated
