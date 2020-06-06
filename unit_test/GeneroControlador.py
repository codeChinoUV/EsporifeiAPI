from app.administracion_de_contenido.modelo.modelos import Genero
from . import BaseTestClass


class GeneroTest(BaseTestClass):

    def test_recuperar_todos_los_generos(self):
        with self.app.app_context():
            generos = Genero.recuperar_todos_los_generos()
            cantidad_generos_disponibles = 2
            self.assertEqual(cantidad_generos_disponibles, len(generos))
