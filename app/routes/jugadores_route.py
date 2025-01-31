from flask import Blueprint

from ..controllers.jugadores_controller import JugadoresController

jugador_bp=Blueprint('jugador_bp',__name__)

jugador_bp.route('/create',methods=['POST'])(JugadoresController.create)
jugador_bp.route('/send_request',methods=['POST'])(JugadoresController.send_request)
jugador_bp.route('/get_all',methods=['GET'])(JugadoresController.get_all)
jugador_bp.route('/get',methods=['POST'])(JugadoresController.get)
jugador_bp.route('/update',methods=['PUT'])(JugadoresController.update)
jugador_bp.route('/accept_invitation',methods=['PUT'])(JugadoresController.accept_invitation)
jugador_bp.route('/delete',methods=['DELETE'])(JugadoresController.delete)