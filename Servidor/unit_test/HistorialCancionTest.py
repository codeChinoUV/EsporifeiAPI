from app.administracion_de_contenido.modelo.modelos import HistorialCancion
from . import BaseTestClass


class HistorialCancionTest(BaseTestClass):

    def test_guardar_historial(self):
        with self.app.app_context():
            historial_cancion = HistorialCancion(id_usuario=1, id_cancion=1)
            historial_cancion.guardar()
            canciones_de_usuario = HistorialCancion.obtener_canciones_de_usuario(1)
            cantidad_canciones_historial = 1
            self.assertEqual(cantidad_canciones_historial, len(canciones_de_usuario))
