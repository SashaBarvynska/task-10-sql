# from flasgger import Swagger
from flask import Flask
from flask_restful import Api
from src.routes import routes
from src.database.connection import db


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    api = Api(app)
    # swagger = Swagger(app)
    db.init_app(app)
    app.register_blueprint(routes)
    return app
