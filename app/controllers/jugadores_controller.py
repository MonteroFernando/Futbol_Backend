from ..models.jugadores_model import Jugadores
from flask import request

class JugadoresController:

    @classmethod
    def create(cls):
        data=request.json
        if not 'name' in data:
            return {'error':'no se encontro el nombre'},400
        category=Jugadores(**data)
        Jugadores.create(category)
        return {'mensaje':'Categoria creada con éxito'},200
    @classmethod
    def get_all(cls):
        categories=Jugadores.get_all()
        return [Jugadores.serialize() for Jugadores in categories],200
    @classmethod
    def get (cls):
        data=request.json
        permitted=('id','name')
        if len(data)>1:
            return {'error':'se ha ingresado mas de un dato'},400
        if not list(data)[0] in permitted:
            return {'error':'Los datos ingresados no son los permitidos'},400
        response=Jugadores.get(data)
        return response.serialize(),200
    @classmethod
    def update(cls):
        data=request.json
        if not 'id' in data:
            return {'mensaje':'No se ingreso el id a modificar'},400
        Jugadores.update(data)
        return {'mensaje':'Categoria modificada con éxito'},200
    @classmethod
    def delete(cls):
        data=request.json
        if not 'id' in data:
            return {'error':'no se ingreso el id a eliminar'},400
        Jugadores.delete(data)
        return {'mensaje':'Se elimino la categoria con éxito'},200