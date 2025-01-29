from app.db.database import DatabaseConnection

def init_db():

    request = DatabaseConnection.fetchone("SHOW DATABASES LIKE 'Futbol_Base'")

    print (request)