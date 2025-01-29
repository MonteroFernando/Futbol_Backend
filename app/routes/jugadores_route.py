from flask import Blueprint

from ..controllers.jugadores_controller import JugadoresController

category_bp=Blueprint('category_bp',__name__)

category_bp.route('/create',methods=['POST'])(JugadoresController.create)
category_bp.route('/get_all',methods=['GET'])(JugadoresController.get_all)
category_bp.route('/get',methods=['GET'])(JugadoresController.get)
category_bp.route('/update',methods=['PUT'])(JugadoresController.update)
category_bp.route('/delete',methods=['DELETE'])(JugadoresController.delete)