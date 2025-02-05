from app.db.database import DatabaseConnection
from config import Config
import os

def init_db(file_name,database_name):

    request = DatabaseConnection.fetchone(f"SHOW DATABASES LIKE '{database_name}';")

    if request is None:
        print ("NO SE ENCONTRO LA BASE DE DATOS, CREANDOLA ....")
        script_dir = os.path.dirname(__file__)  
        sql_file_path = os.path.join(script_dir, file_name)
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

    
        for statement in sql_script.split(';'):
            if statement.strip():
                DatabaseConnection.execute_query(statement)

    else:
        print("BASE DE DATOS ENCONTRADA...")
        
    

