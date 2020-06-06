from app.manejo_de_usuarios.modelo.modelos import Usuario
from app.util.validaciones.modelos.ValidacionUsuario import ValidacionUsuario
from . import BaseTestClass


class UsuarioTest(BaseTestClass):

    def test_registrar_usuario(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba", nombre_usuario="prueba1", contrasena="1235456",
                              correo_electronico="asdf@ghjk.com", tipo_usuario=1)
            usuario.guardar()
            nombre_usuario = Usuario.obtener_usuario(usuario.nombre_usuario).nombre_usuario
            self.assertEqual(usuario.nombre_usuario, nombre_usuario)

    def test_obtener_usuario(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba", nombre_usuario="prueba1", contrasena="1235456",
                              correo_electronico="asdf@ghjk.com", tipo_usuario=1)
            usuario.guardar()
            nombre_usuario = Usuario.obtener_usuario(usuario.nombre_usuario).nombre_usuario
            self.assertEqual(usuario.nombre_usuario, nombre_usuario)

    def test_editar_usuario(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba", nombre_usuario="prueba2", contrasena="1234560",
                              correo_electronico="asd@asdf.com", tipo_usuario=1)
            usuario.guardar()
            usuario.editar(nombre="prueba2", nombre_usuario="prueba3", correo_electronico=None, contrasena=None)
            usuario_modificado = Usuario.obtener_usuario("prueba3")
            self.assertEqual(usuario.id_usuario, usuario_modificado.id_usuario)

    def test_verificar_nombre_usuario_en_uso(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba4", nombre_usuario="prueba4", contrasena="123456",
                              correo_electronico="qwr@sdf.com", tipo_usuario=1)
            nombre_usuario_en_uso = Usuario.verificar_nombre_usuario_disponible(usuario.nombre_usuario)
            esperado = False
            self.assertEqual(esperado, nombre_usuario_en_uso)

    def test_verificar_nombre_usuario_disponible(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba4", nombre_usuario="prueba5", contrasena="123456",
                              correo_electronico="qwr@sdf.com", tipo_usuario=1)
            usuario.guardar()
            nombre_usuario_en_uso = Usuario.verificar_nombre_usuario_disponible("prueba7")
            self.assertEqual(False, nombre_usuario_en_uso)

    def test_verificar_usuario_es_creador_de_contenido(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba4", nombre_usuario="prueba5", contrasena="123456",
                              correo_electronico="qwr@sdf.com", tipo_usuario=1)
            usuario.guardar()
            es_creador_de_contenido = Usuario.validar_usuario_creador_de_contenido(usuario.nombre_usuario)
            self.assertEqual(True, es_creador_de_contenido)

    def test_validar_correo_electronico_disponible(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba4", nombre_usuario="prueba5", contrasena="123456",
                              correo_electronico="qwr@sdf.com", tipo_usuario=1)
            usuario.guardar()
            correo_electronico_disponible = Usuario.validar_correo_electronico_disponible("qwr1@sdf.com")
            self.assertEqual(True, correo_electronico_disponible)

    def test_validar_correo_electronico_ocupado(self):
        with self.app.app_context():
            usuario = Usuario(nombre="prueba4", nombre_usuario="prueba5", contrasena="123456",
                              correo_electronico="qwr@sdf.com", tipo_usuario=1)
            usuario.guardar()
            correo_electronico_disponible = Usuario.validar_correo_electronico_disponible(usuario.correo_electronico)
            self.assertEqual(False, correo_electronico_disponible)

    def test_validar_credenciales(self):
        with self.app.app_context():
            usuario = Usuario.validar_credenciales("creadorDeContenido", "123456")
            self.assertEqual(usuario.nombre_usuario, "creadorDeContenido")


class ValidacionUsuarioTest(BaseTestClass):

    def test_validar_faltan_parametros_requeridos(self):
        with self.app.app_context():
            usuario = Usuario(nombre=None, nombre_usuario=None, contrasena="123456", correo_electronico="asd@sdf.com",
                              tipo_usuario=1)
            error_esperado = "parametros_faltantes"
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_tamano_cadenas_demasiado_corto(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola", nombre_usuario="hola", contrasena="Hola9011.",
                              correo_electronico="asdf@asdf.com", tipo_usuario=1)
            error_esperado = "nombre_usuario_demasiado_corto"
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_tamano_cadenas_demasiado_largo(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola", nombre_usuario="hola123456789010121314157810000", contrasena="Hola9011.",
                              correo_electronico="asdf@asdf.com", tipo_usuario=1)
            error_esperado = "nombre_usuario_demasiado_largo"
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_nombre_usuario_alfanumerico(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo.0 ", contrasena="Hola9011.",
                              correo_electronico="asdf@asdf.com", tipo_usuario=1)
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            error_esperado = "nombre_usuario_no_es_alfanumerico"
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_nombre_usuario_en_uso(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo10", contrasena="Hola9011.",
                              correo_electronico="asdf@asdf.com", tipo_usuario=1)
            usuario.guardar()
            usuario2 = Usuario(nombre="hola como estas", nombre_usuario="holacomo10", contrasena="Hola9011.",
                               correo_electronico="asdf@asdf.com", tipo_usuario=1)
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario2)
            error_esperado = "nombre_usuario_en_uso"
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_contrasena_no_valida(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo", contrasena="hola9011.",
                              correo_electronico="asdf@asdf.com", tipo_usuario=1)
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            error_esperado = "contrasena_no_valida"
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_tipo_usuario_valor_no_valido(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo", contrasena="Hola9011-",
                              correo_electronico="asdf@asdf.com", tipo_usuario="as")
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            error_esperado = "tipo_usuario_valor_no_valido"
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_email_formato_incorrecto(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo", contrasena="Hola9011-",
                              correo_electronico="asdfasdf.com", tipo_usuario=1)
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            error_esperado = "email_formato_incorrecto"
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_email_en_uso(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo", contrasena="Hola9011-",
                              correo_electronico="asdfa@sdf.com", tipo_usuario=1)
            usuario.guardar()
            usuario2 = Usuario(nombre="hola como estas", nombre_usuario="holacomo1", contrasena="Hola9011-",
                               correo_electronico="asdfa@sdf.com", tipo_usuario=1)
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario2)
            error_esperado = "email_en_uso"
            self.assertEqual(error_esperado, error_validacion_usuario[0]['error'])

    def test_validar_registro_usuario_valido(self):
        with self.app.app_context():
            usuario = Usuario(nombre="hola como estas", nombre_usuario="holacomo1", contrasena="Hola9011-",
                              correo_electronico="asdfa@sdf.com", tipo_usuario=1)
            error_validacion_usuario = ValidacionUsuario.validar_registro_usuario(usuario)
            cantidad_errores = 0
            self.assertEqual(cantidad_errores, len(error_validacion_usuario))

    def test_validar_editar_parametros_necesarios(self):
        with self.app.app_context():
            usuario = Usuario(nombre=None, nombre_usuario=None, contrasena=None, correo_electronico=None,
                              tipo_usuario=None)
            error_validacion_edicion = ValidacionUsuario.validar_modificar_usuario(usuario)
            codigo_error = "solicitud_sin_parametros_a_modificar"
            self.assertEqual(codigo_error, error_validacion_edicion['error'])
