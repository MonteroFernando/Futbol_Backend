from ..models.jugadores_model import Jugadores
from ..models.equipos_models import Equipos
from ..models.jugadoresequipos_models import JugadoresEquipos
from datetime import datetime
from flask import request

class JugadoresController:

    @classmethod
    def create(cls):
        
        data = request.json
        required_fields = ['email', 'password', 'nombre', 'apellido', 'edad', 'nivel_habilidad', 'apodo']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400
        
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
    
    @classmethod
    def accept_invitation(cls):
        data = request.json
        required_fields = ['IDJugador', 'IDEquipo']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400

        equipo = Equipos.get({'id':data['IDEquipo']})
        jugador = Jugadores.get({'id':data['IDJugador']})

        if jugador is None:
            return {'error':'No se encontro el Jugador ingresado'},400

        if equipo is None:
            return {'error':'No se encontro el Equipo ingresado'},400
        

                
        relation = JugadoresEquipos.get({'IDEquipo':data['IDEquipo'], 'IDJugador':data['IDJugador']})

        if relation is None:
            return {'error':'No existe la relacion ingresada'},400

        if relation.SolicitudCreadaPor == 'Equipo':
            JugadoresEquipos.update({'IDEquipo':data['IDEEquipo'], 'IDJugador':['IDJugador'], 'EstadoSolicitud':'Aceptada'})
            Equipos.update_qty({'NombreEquipo':equipo.NombreEquipo})
            return {'mensaje': 'Se acepto al jugador y se actualizo el valor del equipo'},200
        else:
            return {'error':'La Solicitud Fue creada por el jugador, el equipo debe aceptar'},400
        
    @classmethod
    def send_request(cls):
        data = request.json
        required_fields = ['IDJugador', 'IDEquipo']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return  {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400
        
        equipo = Equipos.get({'id':data['IDEquipo']})
        jugador = Jugadores.get({'id':data['IDJugador']})

        if jugador is None:
            return  {'error': 'El jugador ingresado no existe'}, 400
        
        if equipo is None:
            return  {'error': 'El equipo ingresado no existe'}, 400
        
        relation = JugadoresEquipos.get({'IDEquipo':data['IDEquipo'], 'IDJugador':data['IDJugador']})

        if relation:
            return {'error':'Ya existe la relacion ingresada'},400
        
        jugadores_equipos = JugadoresEquipos(IDJugador=data['IDJugador'], IDEquipo=equipo.id,
                                            Fecha_Ingreso=datetime.now(), EstadoSolicitud="Pendiente",
                                            SolicitudCreadaPor="jugador")
        JugadoresEquipos.create(jugadores_equipos)
        
        return {'messaje':'Solicitud registrada con éxito'},200
