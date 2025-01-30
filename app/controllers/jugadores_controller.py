from ..models.jugadores_model import Jugadores
from flask import request

class JugadoresController:

    @classmethod
    def create(cls):
        data = request.json
        required_fields = ['email', 'password', 'nombre', 'apellido', 'edad', 'nivel_habilidad', 'apodo']
        
        for field in required_fields:
            if field not in data:
                return {"error": f"Falta el campo: {field}"}, 400
        
        try:
            Jugadores.create(data)
            return {"message": "Jugador creado exitosamente."}, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @classmethod
    def get (cls):
        data=request.json
        permitted=('email', 'id')
        if len(data)>1:
            return {'error':'se ha ingresado mas de un dato'},400
        if not list(data)[0] in permitted:
            return {'error':'Los datos ingresados no son los permitidos'},400
        response=Jugadores.get(data)
        if response is None:
            return {'error':'No se encuentra el email ingresado'}, 400
        return response.serialize(),200

    @classmethod
    def get_all(cls):
        jugadores = Jugadores.get_all()
        return [jugador.serialize() for jugador in jugadores], 200

    @classmethod
    def update(cls):
        data = request.json
        if not 'email' in data:
            return {'error':'no se ingreso el mail del jugador a modificar'},400
        
        jugador = Jugadores.get(data)
        if jugador is None:
            return {"error": "Jugador no encontrado."}, 404

        Jugadores.update(data)
        return {"message": "Jugador actualizado."}, 200

    @classmethod
    def delete(cls):

        data = request.json
        jugador = Jugadores.get(data)
        if jugador is None:
            return {"error": "Jugador no encontrado."}, 404
        
        Jugadores.delete(data)
        return {"message": "Jugador eliminado."}, 200