import unittest
from app import init_app

class JugadorTestCase(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.app = init_app(testing=True)
        self.client = self.app.test_client()
        
    
    def test_get_jugadores(self):
        """Verifica que se puede obtener la lista de jugadores"""
        response = self.client.get('/jugador/get_all')
        self.assertEqual(response.status_code, 200) 
    
    def test_post_jugador(self):
        """Verifica que se puede crear un jugador"""
        nuevo_jugador = {
            "nombre":"Lionel",
            "apellido":"Messi",
            "email": "liomessi@campeonmundial.com",
            "edad": 36,
            "nivel_habilidad": 10,
            "password":"1234",
            "apodo":"Pulga"
        }
        response = self.client.post('/jugador/create', json=nuevo_jugador)
        if response.status_code != 200:
            print("Error response:", response.status_code, response.get_json())

        self.assertEqual(response.status_code, 200, f"error en la respuesta:{response.get_json()}") 

if __name__ == '__main__':
    unittest.main()