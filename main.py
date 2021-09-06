from flask import Flask
from blueprints.books_blueprint import books_blueprint
from blueprints.health_check_blueprint import health_check_blueprint
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(books_blueprint)
    app.register_blueprint(health_check_blueprint)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)