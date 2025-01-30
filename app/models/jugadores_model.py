from app.db.database import DatabaseConnection

class Jugadores:
    _keys = ('id', 'email','password', 'nombre', 'apellido', 'edad', 'nivel_habilidad', 'apodo')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.apellido = kwargs.get('apellido')
        self.nombre = kwargs.get('nombre')
        self.edad = kwargs.get('edad')
        self.nivel_habilidad = kwargs.get('nivel_habilidad')
        self.apodo = kwargs.get('apodo')

    def serialize(self):
        return self.__dict__

    @classmethod
    def create(cls, data):
        # Verificar si el jugador ya existe por email
        query_check = "SELECT COUNT(*) FROM Futbol_Base.jugadores WHERE email = %s"
        params_check = (data['email'],)
        result = DatabaseConnection.fetchone(query_check, params_check)
        
        if result and result[0] > 0:
            raise ValueError("Ya existe un jugador con el mismo email.")
        
        query = """INSERT INTO Futbol_Base.jugadores (email, password, nombre, apellido, edad, nivel_habilidad, apodo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (data['email'], data['password'], data['nombre'], data['apellido'], data['edad'], data['nivel_habilidad'], data['apodo'])
        DatabaseConnection.execute_query(query, params)

    @classmethod
    def get(cls,data):
        key=' ,'.join("{}=%s".format(key) for key in data.keys())
        query=f"SELECT id, email, password, nombre, apellido, edad, nivel_habilidad, apodo FROM Futbol_Base.jugadores WHERE {key}"
        params=tuple(data.values())
        response=DatabaseConnection.fetchone(query,params)
        
        if response is None:
            return None
        else:
            return cls(**dict(zip(cls._keys,response)))


    @classmethod
    def get_all(cls):
        query = "SELECT id, email, password, nombre, apellido, edad, nivel_habilidad, apodo FROM Futbol_Base.jugadores"
        response = DatabaseConnection.fetchall(query)
        
        if not response:
            return []
        else:
            return [cls(**dict(zip(cls._keys, row))) for row in response]

    @classmethod
    def update(cls,data):
        key=' ,'.join("{}=%s".format (key) for key in data.keys() if key!='email')
        query=f"UPDATE futbol_base.jugadores SET {key} WHERE email=%s"
        params=tuple(value for k,value in data.items() if k!='email')+(data['email'],)
        DatabaseConnection.execute_query(query,params)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM Futbol_Base.jugadores WHERE email = %s"
        params = (data['email'],)
        DatabaseConnection.execute_query(query, params)
