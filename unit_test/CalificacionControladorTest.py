from app.administracion_de_contenido.modelo.modelos import Calificacion, Cancion
from app.util.validaciones.modelos.ValidacionCalificacion import ValidacionCalificacion
from . import BaseTestClass


class CalificacionTest(BaseTestClass):

    def test_guardar_calificacion(self):
        with self.app.app_context():
            calificacion_estrellas = 5
            calificacion = Calificacion(id_usuario=2, calificacion_estrellas=calificacion_estrellas, id_cancion=1)
            calificacion.guardar()
            calificacion_guardada = Calificacion.obtener_calificacion(id_cancion=1, id_usuario=2)
            cancion = Cancion.obtener_cancion_por_id(1)
            self.assertEqual(calificacion, calificacion_guardada)
            self.assertEqual(4.0, cancion.calificacion_promedio)

    def test_obtener_calificacion(self):
        with self.app.app_context():
            id_usuario = 1
            calificacion_recuperado = Calificacion.obtener_calificacion(1, id_usuario)
            self.assertEqual(id_usuario, calificacion_recuperado.id_usuario)

    def test_eliminar_calificacion(self):
        with self.app.app_context():
            calificacion_a_eliminar = Calificacion.obtener_calificacion(1, 1)
            calificacion_a_eliminar.eliminar()
            calificacion_eliminada = Calificacion.obtener_calificacion(1, 1)
            calificacion_promedio = 0
            cancion = Cancion.obtener_cancion_por_id(1)
            self.assertEqual(None, calificacion_eliminada)
            self.assertEqual(calificacion_promedio, cancion.calificacion_promedio)

    def test_editar_calificacion(self):
        with self.app.app_context():
            nueva_calificacion = 3
            calificacion = Calificacion.obtener_calificacion(1, 1)
            calificacion.editar_calificacion(nueva_calificacion)
            cancion = Cancion.obtener_cancion_por_id(1)
            self.assertEqual(nueva_calificacion, calificacion.calificacion_estrellas)
            self.assertEqual(nueva_calificacion, cancion.calificacion_promedio)


class ValidacionCalificacionTest(BaseTestClass):

    def test_parametros_requeridos(self):
        with self.app.app_context():
            calificacion = None
            error_campos_requeridos = ValidacionCalificacion.validar_registro_calificacion(calificacion)
            codigo_error = "pametros_faltantes"
            self.assertEqual(codigo_error, error_campos_requeridos['error'])

    def test_calificacion_invalida(self):
        with self.app.app_context():
            calificacion = "hola"
            error_calificacion_invalida = ValidacionCalificacion.validar_registro_calificacion(calificacion)
            codigo_error = "calificacion_estrellas_invalida"
            self.assertEqual(codigo_error, error_calificacion_invalida['error'])

    def test_calificacion_valida(self):
        with self.app.app_context():
            error = None
            error_validacion = ValidacionCalificacion.validar_registro_calificacion(5)
            self.assertEqual(error, error_validacion)

    def test_no_existe_calificacion(self):
        with self.app.app_context():
            codigo_error = "calificacion_inexistente"
            error_no_existe = ValidacionCalificacion.validar_no_existe_calificacion(1, 2)
            self.assertEqual(codigo_error, error_no_existe['error'])

    def test_existe_calificacion(self):
        with self.app.app_context():
            codigo_error = "calificacion_registrada"
            error_existe = ValidacionCalificacion.validar_existe_calificacion(1, 1)
            self.assertEqual(codigo_error, error_existe['error'])
