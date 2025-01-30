from app.db.database import DatabaseConnection

class Partido:
    _keys = ('id', 'Id_EquipoCreador', 'Id_EquipoRival', 'nombre_cancha', 'dirección_cancha', 'fecha', 'hora', 'estado_partido')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.Id_EquipoCreador = kwargs.get('Id_EquipoCreador')
        self.Id_EquipoRival = kwargs.get('Id_EquipoRival')
        self.nombre_cancha = kwargs.get('nombre_cancha')
        self.dirección_cancha = kwargs.get('dirección_cancha')
        self.fecha = kwargs.get('fecha')
        self.hora = kwargs.get('hora')
        self.estado_partido = kwargs.get('estado_partido')

    def serialize(self):
        return self.__dict__

    @classmethod
    def create(cls, data):
        query = """INSERT INTO Partidos (Id_EquipoCreador, Id_EquipoRival, nombre_cancha, dirección_cancha, fecha, hora, estado_partido)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (data['Id_EquipoCreador'], data['Id_EquipoRival'], data['nombre_cancha'], data['dirección_cancha'], data['fecha'], data['hora'], data['estado_partido'])
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def get(cls, partido_id):
        query = "SELECT id, Id_EquipoCreador, Id_EquipoRival, nombre_cancha, dirección_cancha, fecha, hora, estado_partido FROM Partidos WHERE id = %s"
        response = DatabaseConnection.fetchone(query, (partido_id,))
        if response:
            return cls(**dict(zip(cls._keys, response)))
        return None

    @classmethod
    def get_abiertos(cls, nivel_habilidad):
        query = """SELECT id, Id_EquipoCreador, Id_EquipoRival, nombre_cancha, dirección_cancha, fecha, hora, estado_partido
                   FROM Partidos WHERE estado_partido = FALSE AND Id_EquipoRival IS NULL AND nivel_habilidad <= %s"""
        response = DatabaseConnection.fetchall(query, (nivel_habilidad,))
        return [cls(**dict(zip(cls._keys, row))) for row in response]

    @classmethod
    def aceptar_solicitud(cls, partido_id):
        query = """UPDATE Partidos SET estado_partido = TRUE WHERE id = %s"""
        DatabaseConnection.execute_query(query, (partido_id,))

    @classmethod
    def rechazar_solicitud(cls, partido_id):
        query = """UPDATE Partidos SET Id_EquipoRival = NULL WHERE id = %s"""
        DatabaseConnection.execute_query(query, (partido_id,))

    @classmethod
    def cancelar(cls, partido_id):
        query = """DELETE FROM Partidos WHERE id = %s"""
        DatabaseConnection.execute_query(query, (partido_id,))
