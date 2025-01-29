from app.db.database import DatabaseConnection

class Jugadores:
    _keys=('id','email','password','nombre','apellido','edad','nivel_habilidad','apodo')
    def __init__(self,**kwargs):
        self.id = kwargs.get('id')
        self.email=kwargs.get('email')
        self.password=kwargs.get('password')
        self.apellido=kwargs.get('apellido')
        self.edad=kwargs.get('edad')
        self.nivel_habilidad=kwargs.get('nivel_habilidad')
        self.apodo=kwargs.get('apodo')
        self.nombre = kwargs.get('nombre')
        
    
    def serialize(self):
        return self.__dict__
    
    @classmethod
    def create(cls,data):
        query="""INSERT INTO Futbol_Base.jugadores (email,password,nombre,apellido,edad,
        nivel_habilidad, apodo) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        params=(data.email,data.password, data.nombre, data.apellido, data.edad, data.nivel_habilidad,
                data.apodo)
        DatabaseConnection.execute_query(query,params)
    
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
        query="SELECT id, email, password, nombre, apellido, edad, nivel_habilidad, apodo FROM futbol_base.jugadores"
        response=DatabaseConnection.fetchall(query)
        return [cls(**dict(zip(cls._keys,row))) for row in response]
    
    @classmethod
    def update(cls,data):
        key=' ,'.join("{}=%s".format (key) for key in data.keys() if key!='id')
        query=f"UPDATE futbol_base.jugadores SET {key} WHERE id=%s"
        params=tuple(value for k,value in data.items() if k!='id')+(data['id'],)
        DatabaseConnection.execute_query(query,params)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM futbol_base.jugadores WHERE id=%s'
        params = (data['id'],)
        DatabaseConnection.execute_query(query,params)