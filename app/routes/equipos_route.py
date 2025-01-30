from flask import Blueprint
from ..controllers.equipos_controller import EquiposController

equipos_bp = Blueprint('equipos_bp', __name__)

equipos_bp.route('/create', methods=['POST'])(EquiposController.create)
equipos_bp.route('/get_all', methods=['GET'])(EquiposController.get_all)
equipos_bp.route('/get', methods=['GET'])(EquiposController.get)
equipos_bp.route('/update', methods=['PUT'])(EquiposController.update)
equipos_bp.route('/accept_player', methods=['PUT'])(EquiposController.accept_player)
equipos_bp.route('/delete', methods=['DELETE'])(EquiposController.delete)
