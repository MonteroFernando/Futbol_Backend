from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config

def init_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    jwt = JWTManager(app)

    return app


