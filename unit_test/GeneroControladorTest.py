from app.administracion_de_contenido.modelo.modelos import Genero, CreadorDeContenido
from app.util.validaciones.modelos.ValidacionGenero import ValidacionGenero
from . import BaseTestClass


class GeneroTest(BaseTestClass):

    def test_recuperar_todos_los_generos(self):
        with self.app.app_context():
            generos = Genero.recuperar_todos_los_generos()
            cantidad_generos_disponibles = 2
            self.assertEqual(cantidad_generos_disponibles, len(generos))

    def test_obtener_genero_por_id(self):
        with self.app.app_context():
            genero = Genero.obtener_genero_por_id(1)
            self.assertEqual(1, genero.id_genero)

    def test_agregar_creador_de_contenido_a_genero(self):
        with self.app.app_context():
            genero = Genero.obtener_genero_por_id(1)
            creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(1)
            genero.agregar_creador_de_contenido(creador_de_contenido)
            cantidad_creadores_contenido = 1
            self.assertEqual(cantidad_creadores_contenido, len(genero.creadores_de_contenido))

    def test_eliminar_creador_de_contenido(self):
        with self.app.app_context():
            genero = Genero.obtener_genero_por_id(1)
            creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(1)
            genero.agregar_creador_de_contenido(creador_de_contenido)
            genero.eliminar_creador_de_contenido(creador_de_contenido)
            cantidad_creadores_contenido = 0
            self.assertEqual(cantidad_creadores_contenido, len(genero.creadores_de_contenido))


class ValidacionGeneroTest(BaseTestClass):

    def test_campos_requeridos(self):
        with self.app.app_context():
            error_campo_requerido = ValidacionGenero.validar_agregar_genero(None)
            codigo_error = "parametros_faltantes"
            self.assertEqual(codigo_error, error_campo_requerido['error'])

    def test_no_existe_genero(self):
        with self.app.app_context():
            error_no_existe_genero = ValidacionGenero.validar_agregar_genero(4)
            codigo_error = "genero_no_existe"
            self.assertEqual(codigo_error, error_no_existe_genero['error'])

    def test_no_es_numero(self):
        with self.app.app_context():
            error_no_existe_genero = ValidacionGenero.validar_agregar_genero("asdf")
            codigo_error = "id_no_es_entero"
            self.assertEqual(codigo_error, error_no_existe_genero['error'])

    def test_genero_valido(self):
        with self.app.app_context():
            error_no_existe_genero = ValidacionGenero.validar_agregar_genero(1)
            self.assertEqual(None, error_no_existe_genero)
