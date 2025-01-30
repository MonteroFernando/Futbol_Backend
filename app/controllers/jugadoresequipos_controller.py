from flask import request
from ..models.jugadoresequipos_models import JugadoresEquipos
from ..models.equipos_models import Equipos
from ..models.jugadores_model import Jugadores

class JugadoresEquiposController:

    @classmethod
    def create(cls):
        data = request.json
        required_fields = ['email', 'NombreEquipo']

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}, 400

        # Verificar si el jugador existe
        jugador = Jugadores.get({'email': data['email_jugador']})
        if jugador is None:
            return {'error': 'El jugador no existe'}, 404

        # Verificar si el equipo existe
        equipo = Equipos.get({'NombreEquipo': data['nombre_equipo']})
        if equipo is None:
            return {'error': 'El equipo no existe'}, 404
        
        # Verificar si el jugador ya está en el equipo
        existing_membership = JugadoresEquipos.get({'id_jugador': jugador.id, 'id_equipo': equipo.id})
        if existing_membership:
            return {'error': 'El jugador ya está en este equipo'}, 400

        # Crear la relación de jugador y equipo
        membership = JugadoresEquipos(**data)
        JugadoresEquipos.create(membership)

        # Agregar al jugador al equipo, actualizando el promedio de edad y habilidad
        equipo.CantidadJugadores += 1
        equipo.PromedioEdad = (equipo.PromedioEdad * (equipo.CantidadJugadores - 1) + jugador.edad) / equipo.CantidadJugadores
        equipo.PromedioHabilidad = (equipo.PromedioHabilidad * (equipo.CantidadJugadores - 1) + jugador.nivel_habilidad) / equipo.CantidadJugadores
        Equipos.update({'id': equipo.id, 'PromedioEdad': equipo.PromedioEdad, 'PromedioHabilidad': equipo.PromedioHabilidad, 'CantidadJugadores': equipo.CantidadJugadores})

        return {'mensaje': 'Jugador agregado al equipo con éxito'}, 200

    @classmethod
    def get_all(cls):
        response = JugadoresEquipos.get_all()
        return [membership.serialize() for membership in response], 200

    @classmethod
    def get(cls):
        data = request.json
        permitted = ['id_jugador', 'id_equipo']

        if len(data) != 1 or not list(data)[0] in permitted:
            return {'error': 'Los datos ingresados no son los permitidos'}, 400
        
        response = JugadoresEquipos.get(data)
        if response is None:
            return {'error': 'No se encontró la relación entre el jugador y el equipo'}, 404
        
        return response.serialize(), 200

    @classmethod
    def update(cls):
        data = request.json
        required_fields = ['id_jugador', 'id_equipo']

        if not all(field in data for field in required_fields):
            return {'error': 'Faltan los campos id_jugador o id_equipo'}, 400
        
        existing_membership = JugadoresEquipos.get({'id_jugador': data['id_jugador'], 'id_equipo': data['id_equipo']})
        if not existing_membership:
            return {'error': 'No existe esta relación jugador-equipo'}, 404
        
        JugadoresEquipos.update(data)
        return {'mensaje': 'Relación actualizada con éxito'}, 200

    @classmethod
    def delete(cls):
        data = request.json
        required_fields = ['id_jugador', 'id_equipo']

        if not all(field in data for field in required_fields):
            return {'error': 'Faltan los campos id_jugador o id_equipo'}, 400
        
        existing_membership = JugadoresEquipos.get({'id_jugador': data['id_jugador'], 'id_equipo': data['id_equipo']})
        if not existing_membership:
            return {'error': 'No existe esta relación jugador-equipo'}, 404

        # Eliminar al jugador del equipo y actualizar las estadísticas
        JugadoresEquipos.delete(data)

        equipo = Equipos.get({'id': data['id_equipo']})
        jugador = Jugadores.get({'id': data['id_jugador']})

        # Actualizar el promedio y la cantidad de jugadores en el equipo
        equipo.CantidadJugadores -= 1
        equipo.PromedioEdad = (equipo.PromedioEdad * (equipo.CantidadJugadores + 1) - jugador.edad) / equipo.CantidadJugadores if equipo.CantidadJugadores > 0 else 0
        equipo.PromedioHabilidad = (equipo.PromedioHabilidad * (equipo.CantidadJugadores + 1) - jugador.nivel_habilidad) / equipo.CantidadJugadores if equipo.CantidadJugadores > 0 else 0

        Equipos.update({'id': equipo.id, 'PromedioEdad': equipo.PromedioEdad, 'PromedioHabilidad': equipo.PromedioHabilidad, 'CantidadJugadores': equipo.CantidadJugadores})

        return {'mensaje': 'Jugador eliminado del equipo con éxito'}, 200
