from ..models.jugadores_model import Jugadores
from flask import request

class JugadoresController:

    @classmethod
    def create(cls):
        data = request.json
        required_fields = ['email', 'password', 'nombre', 'apellido', 'edad', 'nivel_habilidad', 'apodo']

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400

        data2 = {'email': data["email"]}
        response = Jugadores.get(data2)
        
        if response is None:

            jugador = Jugadores(**data)
            Jugadores.create(jugador)
            return {'mensaje': 'Jugador creado con éxito'}, 200
        
        else:
            return{'mensaje': 'El mail usado ya esta registrado'}, 400
        
    @classmethod
    def get_all(cls):
        response=Jugadores.get_all()
        print (response)
        return [Jugadores.serialize() for Jugadores in response],200
    @classmethod
    def get (cls):
        data=request.json
        permitted=('email', 'id')
        if len(data)>1:
            return {'error':'se ha ingresado mas de un dato'},400
        if not list(data)[0] in permitted:
            return {'error':'Los datos ingresados no son los permitidos'},400
        response=Jugadores.get(data)
        return response.serialize(),200
    @classmethod
    def update(cls):
        data=request.json
        if not 'email' in data:
            return {'mensaje':'No se ingreso el mail a modificar'},400
        Jugadores.update(data)
        return {'mensaje':'Jugador modificado con éxito'},200
    @classmethod
    def delete(cls):
        data=request.json
        if not 'id' in data:
            return {'error':'no se ingreso el id a eliminar'},400
        Jugadores.delete(data)
        return {'mensaje':'Se elimino ej Jugador con éxito'},200