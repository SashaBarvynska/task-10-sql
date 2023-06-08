from flasgger import Swagger
from flask import Flask
from src.api.init_api import init_api
from src.database.connection import db


def create_app(config_object) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    init_api(app)
    Swagger(app)
    db.init_app(app)
    return app
