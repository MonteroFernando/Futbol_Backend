from flask import Blueprint
from app.controllers.partidos_controller import PartidosController

partidos_bp = Blueprint('partidos_bp', __name__)

partidos_bp.route('/create', methods=['POST'])(PartidosController.create)
partidos_bp.route('/get', methods=['GET'])(PartidosController.get)
partidos_bp.route('/get_abiertos', methods=['GET'])(PartidosController.get_abiertos)
partidos_bp.route('/aceptar_solicitud', methods=['PUT'])(PartidosController.aceptar_solicitud)
partidos_bp.route('/rechazar_solicitud', methods=['PUT'])(PartidosController.rechazar_solicitud)
partidos_bp.route('/cancelar', methods=['DELETE'])(PartidosController.cancelar)
