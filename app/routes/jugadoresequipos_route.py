from flask import Blueprint
from ..controllers.jugadoresequipos_controller import JugadoresEquiposController

jugadoresequipos_bp = Blueprint('jugadoresequipos_bp', __name__)

jugadoresequipos_bp.route('/create', methods=['POST'])(JugadoresEquiposController.create)
jugadoresequipos_bp.route('/get_all', methods=['GET'])(JugadoresEquiposController.get_all)
jugadoresequipos_bp.route('/get', methods=['GET'])(JugadoresEquiposController.get)
jugadoresequipos_bp.route('/update', methods=['PUT'])(JugadoresEquiposController.update)
jugadoresequipos_bp.route('/delete', methods=['DELETE'])(JugadoresEquiposController.delete)
