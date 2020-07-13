from app.administracion_de_contenido.modelo.modelos import CreadorDeContenido, Cancion, Genero
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from . import BaseTestClass


class CancionTest(BaseTestClass):

    def test_agregar_creador_de_contenido(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(usuario_id_usuario=2, nombre="Credor de contenido 2",
                                                      es_grupo=True)
            creador_de_contenido.guardar()
            cancion = Cancion.obtener_cancion_por_id(1)
            cancion.agregar_creador_de_contenido(creador_de_contenido)
            cantidad_creadores_de_contenido = 2
            self.assertEqual(cantidad_creadores_de_contenido, len(cancion.creadores_de_contenido))

    def test_obtener_cancion_por_id(self):
        with self.app.app_context():
            id_cancion = 1
            cancion = Cancion.obtener_cancion_por_id(id_cancion)
            self.assertEqual(id_cancion, cancion.id_cancion)

    def test_eliminar_cancion(self):
        with self.app.app_context():
            cancion = Cancion.obtener_cancion_por_id(1)
            cancion.eliminar()
            cancion_eliminada = Cancion.obtener_cancion_por_id(1)
            self.assertEqual(None, cancion_eliminada)

    def test_editar_cancion(self):
        with self.app.app_context():
            nombre = "prueba 2"
            cancion = Cancion.obtener_cancion_por_id(1)
            cancion.editar(nombre)
            self.assertEqual(nombre, cancion.nombre)

    def test_agregar_genero(self):
        with self.app.app_context():
            cancion = Cancion.obtener_cancion_por_id(1)
            genero = Genero.obtener_genero_por_id(1)
            cancion.agregar_genero(genero)
            cantidad_generos = 1
            self.assertEqual(cantidad_generos, len(cancion.generos))

    def test_eliminar_genero(self):
        with self.app.app_context():
            cancion = Cancion.obtener_cancion_por_id(1)
            genero = Genero.obtener_genero_por_id(1)
            cancion.agregar_genero(genero)
            cancion.eliminar_genero(genero)
            cantidad_generos = 0
            self.assertEqual(cantidad_generos, len(cancion.generos))

    def test_buscar(self):
        with self.app.app_context():
            canciones = Cancion.obtener_canciones_por_busqueda("cancion")
            cantidad_de_canciones_que_coinciden = 1
            self.assertEqual(cantidad_de_canciones_que_coinciden, len(canciones))

    def test_eliminar_creador_de_contenido(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(usuario_id_usuario=2, nombre="Credor de contenido 2",
                                                      es_grupo=True)
            creador_de_contenido.guardar()
            cancion = Cancion.obtener_cancion_por_id(1)
            cancion.agregar_creador_de_contenido(creador_de_contenido)
            cancion.eliminar_creador_de_contenido(creador_de_contenido)
            cantidad_creadores_de_contenido = 1
            self.assertEqual(cantidad_creadores_de_contenido, len(cancion.creadores_de_contenido))


class ValidacionCancionTest(BaseTestClass):

    def test_faltan_parametros(self):
        with self.app.app_context():
            cancion = Cancion(nombre=None)
            error_validacion = ValidacionCancion.validar_registro_cancion(cancion)
            codigo_error = "pametros_faltantes"
            self.assertEqual(codigo_error, error_validacion['error'])

    def test_nombre_demasido_corto(self):
        with self.app.app_context():
            cancion = Cancion(nombre="h")
            error_validacion = ValidacionCancion.validar_registro_cancion(cancion)
            codigo_error = "nombre_demasiado_corto"
            self.assertEqual(codigo_error, error_validacion['error'])

    def test_validacion_registro_correcto(self):
        with self.app.app_context():
            cancion = Cancion(nombre="hola amor")
            error_validacion = ValidacionCancion.validar_registro_cancion(cancion)
            self.assertEqual(None, error_validacion)


class CreadorDeContenidoCancionTest(BaseTestClass):

    def test_parametros_requeridos(self):
        with self.app.app_context():
            id_creador_de_contenido = None
            error_parametro_faltante = ValidacionCreadorDeContenido. \
                validar_agregar_creador_de_contenido(id_creador_de_contenido)
            codigo_error = "parametros_faltantes"
            self.assertEqual(codigo_error, error_parametro_faltante['error'])

    def test_id_no_entero(self):
        with self.app.app_context():
            id_creador_de_contenido = "hola"
            error_id_no_entero = ValidacionCreadorDeContenido.validar_agregar_creador_de_contenido(
                id_creador_de_contenido)
            codigo_error = "id_no_es_entero"
            self.assertEqual(codigo_error, error_id_no_entero['error'])

    def test_id_valido(self):
        with self.app.app_context():
            id_creador_de_cotenido = 1
            error_validacion = ValidacionCreadorDeContenido.validar_agregar_creador_de_contenido(id_creador_de_cotenido)
            codigo_error = None
            self.assertEqual(codigo_error, error_validacion)
