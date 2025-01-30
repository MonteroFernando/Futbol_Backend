from flask import request
from ..models.equipos_models import Equipos
from ..models.jugadores_model import Jugadores
from ..models.jugadoresequipos_models import JugadoresEquipos
from ..controllers.jugadoresequipos_controller import JugadoresEquiposController
from datetime import datetime

class EquiposController:

    @classmethod
    def create(cls):
        data = request.json
        required_fields = ['NombreEquipo', 'Logo', 'IDCreador']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400

        # Verificar si ya existe el equipo con el mismo nombre
        equipo_data = {'NombreEquipo': data['NombreEquipo']}
        existing_equipo = Equipos.get(equipo_data)
        if existing_equipo:
            return {'error': 'Ya existe un equipo con ese nombre'}, 400

        jugador = Jugadores.get({'id': data['IDCreador']})
        if jugador is None:
            return {'error': 'El creador no es un jugador válido'}, 400

        # Crear el equipo
        equipo = Equipos(**data)
        Equipos.create(equipo)
        equipo = Equipos.get({'NombreEquipo':data['NombreEquipo']})

        # Asignar al jugador automáticamente
        jugadores_equipo = JugadoresEquipos(IDJugador=data['IDCreador'], IDEquipo=equipo.id,
                                            Fecha_Ingreso=datetime.now(), EstadoSolicitud="Aceptada",
                                            SolicitudCreadaPor="equipo")
        JugadoresEquipos.create(jugadores_equipo)

        # Actualizar el equipo con el jugador
        equipo_data = {'NombreEquipo': equipo.NombreEquipo}
        Equipos.update_qty(equipo_data)

        return {'mensaje': 'Equipo creado y jugador asignado con éxito'}, 200

    @classmethod
    def get_all(cls):
        response = Equipos.get_all()
        return [equipo.serialize() for equipo in response], 200

    @classmethod
    def get(cls):
        data = request.json
        permitted = ('id', 'NombreEquipo')
        if len(data) > 1:
            return {'error': 'Se ha ingresado más de un dato'}, 400
        if not list(data)[0] in permitted:
            return {'error': 'Los datos ingresados no son los permitidos'}, 400
        response = Equipos.get(data)
        if response is None:
            return{'error':'El equipo no se encuentra en la base'},400
        return response.serialize(), 200

    @classmethod
    def update(cls):
        data = request.json
        if not 'NombreEquipo' in data:
            return {'error': 'El nombre del equipo es requerido'}, 400
        
        if not any(field in data for field in ['Logo', 'IDCreador', 'EquipoCompleto', 'Promedio_Habilidad', 'Promedio_Edad','CantidadJugadores']):
            return {'error': 'Se requiere al menos uno de los campos: Logo, IDCreador'}, 400
        
        Equipos.update(data)
        return {'mensaje': 'Equipo modificado con éxito'}, 200

    @classmethod
    def delete(cls):
        data = request.json
        if not 'NombreEquipo' in data:
            return {'error': 'El nombre del equipo es requerido'}, 400
        Equipos.delete(data)
        return {'mensaje': 'Equipo eliminado con éxito'}, 200
    
    @classmethod
    def accept_player(cls):
        data = request.json
        required_fields = ['IDJugador', 'IDEquipo', 'IDCreador']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400

        equipo = Equipos.get({'id':data['IDEquipo']})
        jugador = Jugadores.get({'id':data['IDJugador']})

        if jugador is None:
            return {'error':'No se encontro el Jugador ingresado'},400

        if equipo is None:
            return {'error':'No se encontro el Equipo ingresado'},400
        

        if equipo.IDCreador != data ['IDCreador']:
            return {'error':'El usuario no es el creador del equipo'},400
        
        relation = JugadoresEquipos.get({'IDEquipo':data['IDEquipo'], 'IDJugador':data['IDJugador']})

        if relation is None:
            return {'error':'No existe la relacion ingresada'},400

        if relation.SolicitudCreadaPor == 'Jugador':
            JugadoresEquipos.update({'IDEquipo':data['IDEEquipo'], 'IDJugador':['IDJugador'], 'EstadoSolicitud':'Aceptada'})
            Equipos.update_qty({'NombreEquipo':equipo.NombreEquipo})
            return {'mensaje': 'Se acepto al jugador y se actualizo el valor del equipo'},200
        else:
            return {'error':'La Solicitud Fue creada por el equipo, el jugador debe aceptar'},400
        
    @classmethod
    def invite_player(cls):
        data = request.json
        required_fields = ['IDJugador', 'IDEquipo', 'IDCreador']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return  {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400
        
        equipo = Equipos.get({'id':data['IDEquipo']})
        jugador = Jugadores.get({'id':data['IDJugador']})

        if jugador is None:
            return  {'error': 'El jugador ingresado no existe'}, 400
        
        if equipo is None:
            return  {'error': 'El equipo ingresado no existe'}, 400
        
        if equipo.IDCreador != data['IDCreador']:
            return {'error':'El Equipo ingresado no pertenece al jugador'}, 400
        
        jugadores_equipos = JugadoresEquipos(IDJugador=data['IDCreador'], IDEquipo=equipo.id,
                                            Fecha_Ingreso=datetime.now(), EstadoSolicitud="Pendiente",
                                            SolicitudCreadaPor="equipo")
        JugadoresEquipos.create(jugadores_equipos)
        
        return {'messaje':'Solicitud registrada con éxito'},200

        



    
    
