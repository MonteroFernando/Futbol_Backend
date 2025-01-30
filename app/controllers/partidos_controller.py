from flask import request, jsonify
from app.models.partidos_models import Partido

class PartidosController:
    @staticmethod
    def create():
        data = request.get_json()
        try:
            Partido.create(data)
            return jsonify({"message": "Partido creado exitosamente."}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get():
        partido_id = request.args.get('id')
        partido = Partido.get(partido_id)
        if partido:
            return jsonify(partido.serialize())
        return jsonify({"message": "Partido no encontrado."}), 404

    @staticmethod
    def get_abiertos():
        nivel_habilidad = request.args.get('nivel_habilidad')
        partidos = Partido.get_abiertos(nivel_habilidad)
        return jsonify([partido.serialize() for partido in partidos])

    @staticmethod
    def aceptar_solicitud():
        partido_id = request.args.get('id')
        try:
            Partido.aceptar_solicitud(partido_id)
            return jsonify({"message": "Solicitud aceptada. El partido está listo para jugar."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def rechazar_solicitud():
        partido_id = request.args.get('id')
        try:
            Partido.rechazar_solicitud(partido_id)
            return jsonify({"message": "Solicitud rechazada. El partido está abierto."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def cancelar():
        partido_id = request.args.get('id')
        try:
            Partido.cancelar(partido_id)
            return jsonify({"message": "Partido cancelado."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
