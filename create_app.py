from flask import Flask
from blueprints.books_blueprint import books_blueprint
from blueprints.health_check_blueprint import health_check_blueprint
from blueprints.user_blueprint import users_blueprint
from mongoengine import connect
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    connect(
        db=config_class.DB_NAME,
        host=config_class.DB_HOST,
        port=int(config_class.DB_PORT),
    )

    app.register_blueprint(books_blueprint)
    app.register_blueprint(health_check_blueprint)
    app.register_blueprint(users_blueprint)

    return app