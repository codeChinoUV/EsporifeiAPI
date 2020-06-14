from app.administracion_de_contenido.modelo.modelos import ListaDeReproduccion
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
            cantidad_lista_reproduccion = 1
            self.assertEqual(cantidad_lista_reproduccion, len(listas_de_reproduccion_del_usuario))


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
