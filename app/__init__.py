from flask import Flask
from flask_cors import CORS
from config import Config, TestingConfig
from app.db.database import DatabaseConnection
from app.db.init_database import init_db

from .routes.jugadores_route import jugador_bp
from .routes.equipos_route import equipos_bp
from .routes.jugadoresequipos_route import jugadoresequipos_bp
from .routes.partidos_routes import partidos_bp


def init_app(testing=False):
    app = Flask(__name__)

    CORS(app, supports_credentials=True)

    app.config.from_object(Config)

    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)
        
    filename = 'create_dbTest.sql' if testing else 'create_dataBase.sql'
    
    try:
        DatabaseConnection.set_config(app.config)
        init_db(filename, app.config["DATABASE_NAME"])
    except Exception as e:
        app.logger.error(f"Error al inicializar la base de datos: {e}")

    app.register_blueprint(jugador_bp,url_prefix='/jugador')
    app.register_blueprint(equipos_bp,url_prefix='/equipo')
    app.register_blueprint(jugadoresequipos_bp,url_prefix='/jugadoresequipos')
    app.register_blueprint(partidos_bp,url_prefix='/partidos')

    return app


