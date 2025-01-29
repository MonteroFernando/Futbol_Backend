from flask import Flask
from flask_cors import CORS
from config import Config
from app.db.database import DatabaseConnection
from app.db.init_database import init_db

def init_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True)

    app.config.from_object(Config)

    try:
        DatabaseConnection.set_config(app.config)
        init_db()
    except Exception as e:
        app.logger.error(f"Error al inicializar la base de datos: {e}")

    

    return app


