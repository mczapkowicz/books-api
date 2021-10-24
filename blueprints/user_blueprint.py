import datetime
import jwt
import os
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from core.rate_limiter import limiter
from models.users import Users

users_blueprint = Blueprint('users_blueprint', __name__)

limiter.limit("10/minute")(users_blueprint)


@users_blueprint.route('/register', methods=['POST'])
def add_user():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    name = request.form.get('name', None)

    if email is None:
        return jsonify({"message": "email field is missing"}), 400
    if password is None:
        return jsonify({"message": "password field is missing"}), 400
    if name is None:
        return jsonify({"message": "name field is missing"}), 400

    hashed_password = generate_password_hash(password)
    user = Users(email=email, password=hashed_password)
    user.save()
    return jsonify({"message": 'User added'})


@users_blueprint.route('/login', methods=['GET'])
def login_user():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if email is None:
        return jsonify({"message": "email field is missing"}), 400
    if password is None:
        return jsonify({"message": "password field is missing"}), 400

    user = Users.objects(email=email).first()
    if check_password_hash(user.password, password):
        encoded = jwt.encode({
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            os.environ.get("SALT"),
            algorithm="HS256"
        )
        return jsonify({"token": encoded}), 400
    else:
        return jsonify({"message": "user not exit"}), 404
