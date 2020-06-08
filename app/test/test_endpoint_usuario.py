from . import BaseTestClass
from ..manejo_de_usuarios.modelo.modelos import Usuario


class LoginControladorTestCase(BaseTestClass):

    def test_validar_credenciales_incorrectas(self):
        with self.app.app_context():
            usuario_logeado = Usuario.validar_credenciales("holacomoestas", "123456")
            self.assertEqual(None, usuario_logeado)

    def test_validar_credenciales_correctas(self):
        with self.app.app_context():
            nombre_usuario = "creadorDeContenido"
            usuario_logeado = Usuario.validar_credenciales(nombre_usuario, "123456")
            self.assertEqual(nombre_usuario, usuario_logeado.nombre_usuario)
