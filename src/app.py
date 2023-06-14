from flask import Flask
from src.api.init_api import init_api
from src.database.connection import db
from src.swagger.init_swagger import init_swagger


def create_app(config_object) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    init_api(app)
    init_swagger(app)
    db.init_app(app)
    return app
