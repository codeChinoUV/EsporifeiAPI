from app.administracion_de_contenido.modelo.modelos import ListaDeReproduccion, Cancion
from app.util.validaciones.modelos.ValidacionListaDeReproduccion import ValidacionListaDeReproduccion
from . import BaseTestClass


class ListaDeReproduccionTest(BaseTestClass):

    def test_guardar_lista_de_reproduccion(self):
        with self.app.app_context():
            lista_de_reprodudccion = ListaDeReproduccion(usuario_id=1, nombre="Lista de reproduccion prueba")
            lista_de_reprodudccion.guardar()
            id_registrado = 1
            self.assertEqual(id_registrado, lista_de_reprodudccion.usuario_id)

    def test_obtener_listas_de_reproduccion_de_usuarios(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(usuario_id=1, nombre="Lista de reproduccion prueba")
            lista_de_reproduccion.guardar()
            listas_de_reproduccion_del_usuario = ListaDeReproduccion.obtener_listas_de_reproduccion_de_usuario(1)
            cantidad_lista_reproduccion = 2
            self.assertEqual(cantidad_lista_reproduccion, len(listas_de_reproduccion_del_usuario))

    def test_editar_lista_de_reproduccion(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(usuario_id=1, nombre="Lista de reproduccion prueba")
            lista_de_reproduccion.guardar()
            nuevo_nombre = "Lista de prueba 2"
            lista_de_reproduccion.editar(nuevo_nombre, None)
            self.assertEqual(nuevo_nombre, lista_de_reproduccion.nombre)

    def test_eliminar_lista_de_reproduccion(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(usuario_id=1, nombre="Lista de reproduccion prueba")
            lista_de_reproduccion.guardar()
            lista_de_reproduccion.eliminar()
            lista_eliminada = ListaDeReproduccion.obtener_lista_de_reproduccion(2)
            self.assertEqual(None, lista_eliminada)

    def test_agregar_cancion(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(1)
            cancion = Cancion.obtener_cancion_por_id(1)
            lista_de_reproduccion.agregar_cancion(cancion)
            cantidad_de_canciones = 1
            self.assertEqual(cantidad_de_canciones, len(lista_de_reproduccion.canciones))

    def test_quitar_cancion(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(1)
            cancion = Cancion.obtener_cancion_por_id(1)
            lista_de_reproduccion.agregar_cancion(cancion)
            lista_de_reproduccion.quitar_cancion(cancion)
            cantidad_de_canciones = 0
            self.assertEqual(cantidad_de_canciones, len(lista_de_reproduccion.canciones))


class ValidacionListaDeReproduccionTest(BaseTestClass):

    def test_parametros_requeridos(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre=None)
            errores_validacion = ValidacionListaDeReproduccion. \
                validar_registro_lista_de_reproduccion(lista_de_reproduccion)
            codigo_de_error = "pametros_faltantes"
            self.assertEqual(codigo_de_error, errores_validacion[0]['error'])

    def test_nombre_demasido_corto(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre="asd")
            errores_nombre_demasiado_corto = ValidacionListaDeReproduccion \
                .validar_registro_lista_de_reproduccion(lista_de_reproduccion)
            codigo_error = "nombre_demasiado_corto"
            self.assertEqual(codigo_error, errores_nombre_demasiado_corto[0]['error'])

    def test_registro_valido(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre="Prueba de lista de reproduccion")
            errores_validacion = ValidacionListaDeReproduccion \
                .validar_registro_lista_de_reproduccion(lista_de_reproduccion)
            cantidad_errores = 0
            self.assertEqual(cantidad_errores, len(errores_validacion))

    def test_no_existe_lista_de_reproduccion(self):
        with self.app.app_context():
            error_no_existe = ValidacionListaDeReproduccion.validar_no_existe_lista_de_reproduccion(2)
            codigo_error = "lista_reproduccion_inexistente"
            self.assertEqual(codigo_error, error_no_existe['error'])

    def test_existe_lista_de_reproduccion(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre="Prueba de lista de reproduccion", usuario_id=1)
            lista_de_reproduccion.guardar()
            codigo_de_error = None
            error_no_existe = ValidacionListaDeReproduccion.validar_no_existe_lista_de_reproduccion(1)
            self.assertEqual(codigo_de_error, error_no_existe)

    def test_no_es_dueno(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre="Prueba", usuario_id=2)
            lista_de_reproduccion.guardar()
            error_no_es_dueno = ValidacionListaDeReproduccion.validar_usuario_es_dueno_de_lista_de_reproduccion(2, 1)
            codigo_error = "operacion_no_permitida"
            self.assertEqual(codigo_error, error_no_es_dueno['error'])

    def test_es_dueno(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre="Prueba", usuario_id=1)
            lista_de_reproduccion.guardar()
            error_no_es_dueno = ValidacionListaDeReproduccion.validar_usuario_es_dueno_de_lista_de_reproduccion(1, 1)
            codigo_error = None
            self.assertEqual(codigo_error, error_no_es_dueno)

    def test_solicitud_vacia(self):
        with self.app.app_context():
            lista_de_reproduccion = ListaDeReproduccion(nombre=None, descripcion=None)
            error_sin_parametros = ValidacionListaDeReproduccion. \
                validar_edicion_lista_de_reproduccion(lista_de_reproduccion)
            codigo_error = "solicitud_sin_parametros_a_modificar"
            self.assertEqual(codigo_error, error_sin_parametros[0]['error'])

    def test_agregar_cancion_parametros_faltantes(self):
        with self.app.app_context():
            id_cancion = None
            error_parametros_faltantes = ValidacionListaDeReproduccion.validar_agregar_cancion(id_cancion)
            codigo_error = "pametros_faltantes"
            self.assertEqual(codigo_error, error_parametros_faltantes['error'])

    def test_agregar_cancion_id_no_es_entero(self):
        with self.app.app_context():
            id_cancion = "asf"
            error_id_no_entero = ValidacionListaDeReproduccion.validar_agregar_cancion(id_cancion)
            codigo_error = "id_no_es_entero"
            self.assertEqual(codigo_error, error_id_no_entero['error'])

    def test_agregar_cancion_cancion_inexistente(self):
        with self.app.app_context():
            id_cancion = 400
            error_cancion_no_existe = ValidacionListaDeReproduccion.validar_agregar_cancion(id_cancion)
            codigo_error = "cancion_inexistente"
            self.assertEqual(codigo_error, error_cancion_no_existe['error'])

    def test_lista_no_tiene_cancion(self):
        with self.app.app_context():
            validacion_no_tiene_cancion = ValidacionListaDeReproduccion. \
                validar_existe_cancion_en_lista_de_reproduccion(1, 1)
            codigo_error = "cancion_inexistente"
            self.assertEqual(codigo_error, validacion_no_tiene_cancion['error'])

    def test_lista_tiene_cancion(self):
        with self.app.app_context():
            lista_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(1)
            cancion = Cancion.obtener_cancion_por_id(1)
            lista_reproduccion.agregar_cancion(cancion)
            validacion_tiene_cancion = ValidacionListaDeReproduccion. \
                validar_existe_cancion_en_lista_de_reproduccion(1, 1)
            codigo_error = None
            self.assertEqual(codigo_error, validacion_tiene_cancion)
