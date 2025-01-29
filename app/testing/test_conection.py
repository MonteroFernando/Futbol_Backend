import mysql.connector

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="Nano1984*"
    )
    if connection.is_connected():
        print("Conexión exitosa a MySQL.")
    else:
        print("Fallo al conectar a MySQL.")
except mysql.connector.Error as e:
    print(f"Error al conectar a MySQL: {e}")
finally:
    if connection and connection.is_connected():
        connection.close()
        print("Conexión cerrada.")
