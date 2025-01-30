from app.db.database import DatabaseConnection

class Equipos:
    _keys = ('id', 'NombreEquipo', 'Logo', 'IDCreador', 'EquipoCompleto', 'Promedio_Habilidad', 'Promedio_Edad', 'CantidadJugadores')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.NombreEquipo = kwargs.get('NombreEquipo')
        self.Logo = kwargs.get('Logo')
        self.IDCreador = kwargs.get('IDCreador')
        self.EquipoCompleto = kwargs.get('EquipoCompleto', False)
        self.Promedio_Habilidad = kwargs.get('Promedio_Habilidad',0)
        self.Promedio_Edad = kwargs.get('Promedio_Edad',0)
        self.CantidadJugadores = kwargs.get('CantidadJugadores', 0)

    def serialize(self):
        return self.__dict__

    @classmethod
    def create(cls, data):
        query = """INSERT INTO Futbol_Base.Equipos (NombreEquipo, Logo, IDCreador, EquipoCompleto, Promedio_Habilidad, Promedio_Edad, CantidadJugadores) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (
                    data.NombreEquipo, data.Logo, data.IDCreador, data.EquipoCompleto,
                    data.Promedio_Habilidad, data.Promedio_Edad, data.CantidadJugadores
                )
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def get(cls, data):
        if not data:
            raise ValueError("Se requiere al menos un campo para la búsqueda.")

        conditions = ' AND '.join(f"{key}=%s" for key in data)
        query = f"SELECT {', '.join(cls._keys)} FROM Futbol_Base.Equipos WHERE {conditions}"
        params = tuple(data.values())

        response = DatabaseConnection.fetchone(query, params)
        if response is None:
            return None
        return cls(**dict(zip(cls._keys, response))) if response else None

    @classmethod
    def get_all(cls):
        query = "SELECT id, NombreEquipo, Logo, IDCreador, EquipoCompleto, Promedio_Habilidad, Promedio_Edad, CantidadJugadores FROM Futbol_Base.Equipos"
        response = DatabaseConnection.fetchall(query)
        return [cls(**dict(zip(cls._keys, row))) for row in response]

    @classmethod
    def update(cls, data):
        if 'NombreEquipo' not in data:
            raise ValueError("Se requiere NombreEquipo para actualizar.")

        key_values = ', '.join(f"{key}=%s" for key in data if key != 'NombreEquipo')
        query = f"UPDATE Futbol_Base.Equipos SET {key_values} WHERE NombreEquipo=%s"

        params = tuple(data[key] for key in data if key != 'NombreEquipo') + (data['NombreEquipo'],)
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM Futbol_Base.Equipos WHERE NombreEquipo=%s"
        params = (data['NombreEquipo'],)
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def update_qty(cls,NombreEquipo):
        equipo = cls.get(NombreEquipo)

        queryprom = """SELECT COUNT(J.id) AS CantidadJugadores, AVG(J.edad) AS PromedioEdad,
                        AVG(J.nivel_habilidad) AS PromedioHabilidad
                        FROM Futbol_Base.Equipos E
                        JOIN Futbol_Base.JugadoresEquipos JE ON E.id = JE.IDEquipo
                        JOIN Futbol_Base.Jugadores J ON JE.IDJugador = J.id
                        WHERE E.id = %s AND JE.EstadoSolicitud = 'Aceptada'
                        GROUP BY E.id;"""
        
        prom=DatabaseConnection.fetchone(queryprom, (equipo.id,))

        if prom[0] >=5:
            estado = True
        else:
            estado = False
            
        data = {
                'NombreEquipo':equipo.NombreEquipo, 
                'CantidadJugadores':prom[0],
                'Promedio_Edad':prom[1],
                'Promedio_Habilidad':prom[2],
                'EquipoCompleto':estado
                
                }
        cls.update(data)
        
        

        
