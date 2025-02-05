from app.db.database import DatabaseConnection

class JugadoresEquipos:
    _keys = ('IDJugador', 'IDEquipo', 'Fecha_Ingreso', 'EstadoSolicitud', 'SolicitudCreadaPor')

    def __init__(self, **kwargs):
        self.IDJugador = kwargs.get('IDJugador')
        self.IDEquipo = kwargs.get('IDEquipo')
        self.Fecha_Ingreso = kwargs.get('Fecha_Ingreso')
        self.EstadoSolicitud = kwargs.get('EstadoSolicitud')
        self.SolicitudCreadaPor = kwargs.get('SolicitudCreadaPor')

    def serialize(self):
        return self.__dict__

    @classmethod
    def create(cls, data):
        query = """INSERT INTO JugadoresEquipos (IDJugador, IDEquipo, Fecha_Ingreso, EstadoSolicitud, SolicitudCreadaPor) 
                   VALUES (%s, %s, %s, %s, %s)"""
        params = (data.IDJugador, data.IDEquipo, data.Fecha_Ingreso, data.EstadoSolicitud, data.SolicitudCreadaPor)
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def get(cls, data):
        if not data:
            raise ValueError("Se requiere al menos un campo para la búsqueda.")
        
        conditions = ' AND '.join(f"{key}=%s" for key in data)

        query = f"SELECT IDJugador, IDEquipo, Fecha_Ingreso, EstadoSolicitud, SolicitudCreadaPor FROM JugadoresEquipos WHERE {conditions}"
        params = tuple(data.values())
        
        response = DatabaseConnection.fetchone(query, params)
        if response is None:
            return None
        else:
            return cls(**dict(zip(cls._keys, response)))

    @classmethod
    def get_all(cls,data):
        if not data:
            query = "SELECT IDJugador, IDEquipo, Fecha_Ingreso, EstadoSolicitud, SolicitudCreadaPor FROM JugadoresEquipos"
            response = DatabaseConnection.fetchall(query)
            
        else:
            key = ' AND '.join("{}=%s".format(key) for key in data.keys())
            query = f"SELECT IDJugador, IDEquipo, Fecha_Ingreso, EstadoSolicitud, SolicitudCreadaPor FROM JugadoresEquipos WHERE {key}"    
            params = tuple(data.values())
            response = DatabaseConnection.fetchall(query, params)
        return [cls(**dict(zip(cls._keys, row))) for row in response]

    @classmethod
    def update(cls, data):
        key = ' ,'.join("{}=%s".format(key) for key in data.keys() if key != 'IDJugador' and key != 'IDEquipo')
        query = f"UPDATE JugadoresEquipos SET {key} WHERE IDJugador=%s AND IDEquipo=%s"
        params = tuple(value for k, value in data.items() if k != 'IDJugador' and k != 'IDEquipo') + (data['IDJugador'], data['IDEquipo'])
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM JugadoresEquipos WHERE IDJugador=%s AND IDEquipo=%s"
        params = (data['IDJugador'], data['IDEquipo'])
        DatabaseConnection.execute_query(query, params)
