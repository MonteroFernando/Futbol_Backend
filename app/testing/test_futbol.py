import unittest
from app import init_app
from app.db.database import DatabaseConnection

class FutbolTestCase(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.app = init_app(testing=True)
        self.client = self.app.test_client()
        
    def test_case_futbol(self):
        
        jugadores = [
        {"nombre": "Lionel", "apellido": "Messi", "email": "liomessi@campeonmundial.com", "edad": 36, "nivel_habilidad": 10, "password": "1234", "apodo": "Pulga"},
        {"nombre": "Angel", "apellido": "Di Maria", "email": "angelito@campeonmundial.com", "edad": 36, "nivel_habilidad": 10, "password": "1234", "apodo": "Fideo"},
        {"nombre": "Emiliano", "apellido": "Martinez", "email": "dibu@campeonmundial.com", "edad": 32, "nivel_habilidad": 8, "password": "1234", "apodo": "Dibu"}
             ]

        
        for jugador in jugadores:
            response = self.client.post('/jugador/create', json=jugador)
            if response.status_code != 200:

                print("Código de estado:", response.status_code)
                print("Cuerpo de la respuesta:", response.get_json())
            
            self.assertEqual(response.status_code, 201, f"Error al crear jugador: {response.get_json()}")
            print(f"\u2705 Jugador creado exitosamente: {jugador['nombre']} {jugador['apellido']} ({jugador['email']})")

    
        """Verifica que se puede obtener la lista de jugadores"""
        response = self.client.get('/jugador/get_all')
        if response.status_code != 200:

            print("Código de estado:", response.status_code)
            print("Cuerpo de la respuesta:", response.get_json())

        self.assertEqual(response.status_code, 200)
        print(f"\u2705 Lista de jugadores recupera exitosamente")

        """Crea un equipo generado por el jugador 1"""
        nuevo_equipo = {
            "NombreEquipo":"Argentina",
            "Logo":"AFA",
            "IDCreador":1
        }
        response= self.client.post('/equipo/create',json = nuevo_equipo)
        if response.status_code != 200:

            print("Código de estado:", response.status_code)
            print("Cuerpo de la respuesta:", response.get_json())
        self.assertEqual(response.status_code, 200, f"Error al crear el equipo: {response.get_json()}")

        print (f"\u2705 Equipo creado exitosamente y jugador 1 asignado al equipo")

        """Invitacion a un Jugador a ingresar al equipo"""
        nueva_invitacion = {
            "IDJugador":2,
            "IDEquipo":1,
            "IDCreador":1
        }
        response= self.client.post('/equipo/invite_player',json = nueva_invitacion)
        if response.status_code != 200:

            print("Código de estado:", response.status_code)
            print("Cuerpo de la respuesta:", response.get_json())
        self.assertEqual(response.status_code, 200, f"Error al invitar un jugador: {response.get_json()}")

        print (f"\u2705 Invitacion enviada con exito desde el equipo1 al jugador 2, esperando respuesta")
        
        """Envio de solicitud de un jugador al equipo"""
        nueva_solicitud = {
            "IDJugador":3,
            "IDEquipo":1
        }
        response= self.client.post('/jugador/send_request',json = nueva_solicitud)
        if response.status_code != 200:

            print("Código de estado:", response.status_code)
            print("Cuerpo de la respuesta:", response.get_json())
        self.assertEqual(response.status_code, 200, f"Error al solicitar ingreso: {response.get_json()}")

        print (f"\u2705 Solicitud enviada con exito desde el jugador3 al equipo1, esperando respuesta")
        
        """Aceptacion del jugador 2 al equipo 1"""
        acepta_equipo = {
            "IDJugador":3,
            "IDEquipo":1,
            "IDCreador":1
        }
        response= self.client.put('/equipo/accept_player',json = acepta_equipo)
        if response.status_code != 200:

            print("Código de estado:", response.status_code)
            print("Cuerpo de la respuesta:", response.get_json())
        self.assertEqual(response.status_code, 200, f"Error al aceptar un jugador: {response.get_json()}")

        print (f"\u2705 Solicitu aceptado por el equipo 1 al jugador 3")
        
        
        """Aceptacion del jugador 2 al equipo 1"""
        acepta_jugador = {
            "IDJugador":2,
            "IDEquipo":1
        }
        response= self.client.put('/jugador/accept_invitation',json = acepta_jugador)
        if response.status_code != 200:

            print("Código de estado:", response.status_code)
            print("Cuerpo de la respuesta:", response.get_json())
        self.assertEqual(response.status_code, 200, f"Error al aceptar invitacion: {response.get_json()}")

        print (f"\u2705 Invitacion del equipo 1 al jugador 2, aceptada")


        


    
if __name__ == '__main__':
    unittest.main()