from app.manejo_de_usuarios.modelo.enum.enums import TipoUsuario
from app.manejo_de_usuarios.modelo.modelos import Usuario
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from . import BaseTestClass


class AlbumControlador(BaseTestClass):

    def test_validar_creador_de_contenido_no_existe(self):
        with self.app.app_context():
            usuario_actual = Usuario(nombre_usuario="creadorDeContenido", contrasena="123456",
                                     tipo_usuario=TipoUsuario.CreadorDeContenido, correo_electronico="ad@ad.com")
            error = ValidacionCreadorDeContenido \
                .validar_creador_de_contenido_existe_a_partir_de_usuario(usuario_actual)
            codigo_error = "usuario_no_tiene_un_creador_de_contenido"
            self.assertEqual(codigo_error, error['error'])
