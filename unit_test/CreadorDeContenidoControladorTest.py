from app.administracion_de_contenido.modelo.modelos import CreadorDeContenido
from app.manejo_de_usuarios.modelo.modelos import Usuario
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from . import BaseTestClass


class CreadorDeContenidoTest(BaseTestClass):

    def test_guardar(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre="prueba1", es_grupo=False, usuario_id_usuario=3)
            creador_de_contenido.guardar()
            creador_de_contenido_recuperado = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(3)
            self.assertEqual(creador_de_contenido.id_creador_de_contenido,
                             creador_de_contenido_recuperado.id_creador_de_contenido)

    def test_editar(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre="prueba1", es_grupo=False, usuario_id_usuario=3)
            creador_de_contenido.guardar()
            creador_de_contenido.editar(nombre="prueba2", biografia=None, es_grupo=True)
            creador_de_contenido_recuperado = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(3)
            self.assertEqual(creador_de_contenido.nombre, creador_de_contenido_recuperado.nombre)

    def test_verificar_usuario_no_tiene_creador_de_contenido(self):
        with self.app.app_context():
            usuario_tiene_perfil = CreadorDeContenido.verificar_usuario_tiene_creador_contenido_registrado(3)
            self.assertEqual(False, usuario_tiene_perfil)

    def test_verificar_usuario_tiene_creador_de_contenido(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre="prueba3", es_grupo=False, usuario_id_usuario=3)
            creador_de_contenido.guardar()
            usuario_tiene_perfil = CreadorDeContenido.verificar_usuario_tiene_creador_contenido_registrado(3)
            self.assertEqual(True, usuario_tiene_perfil)

    def test_verificar_no_existe_creador_de_contenido(self):
        with self.app.app_context():
            existe_creador_de_contenido = CreadorDeContenido.verificar_existe_creador_contenido(3)
            self.assertEqual(False, existe_creador_de_contenido)

    def test_verficar_existe_creador_de_contenido(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre="prueba", es_grupo=True, usuario_id_usuario=3)
            creador_de_contenido.guardar()
            existe_creador_de_contenido = CreadorDeContenido.verificar_existe_creador_contenido(2)
            self.assertEqual(True, existe_creador_de_contenido)

    def test_obtener_creador_de_contenido_por_id(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(1)
            self.assertEqual(1, creador_de_contenido.id_creador_de_contenido)

    def test_obtener_creador_de_contenido_por_id_usuario(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(1)
            self.assertEqual(1, creador_de_contenido.usuario_id_usuario)

    def test_obtener_creador_de_contenido_por_busqueda(self):
        with self.app.app_context():
            cadena_busqueda = "pru"
            creadores_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_busqueda(cadena_busqueda)
            self.assertEqual(1, len(creadores_de_contenido))


class ValidacionCreadorDeContenidoTest(BaseTestClass):

    def test_validar_parametros_requeridos(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre=None, es_grupo=None)
            errores_creador_de_contenido = ValidacionCreadorDeContenido. \
                validar_registro_creador_de_contenido(creador_de_contenido)
            codigo_error = "parametros_faltantes"
            self.assertEqual(codigo_error, errores_creador_de_contenido[0]['error'])

    def test_validar_tamano_nombre_demasido_corto(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre="asdf", es_grupo=False)
            errores_creador_de_contenido = ValidacionCreadorDeContenido. \
                validar_registro_creador_de_contenido(creador_de_contenido)
            codigo_error = "nombre_demasiado_corto"
            self.assertEqual(codigo_error, errores_creador_de_contenido[0]['error'])

    def test_json_invalido(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre="hola como", es_grupo="tal vez")
            errores_creador_de_contenido = ValidacionCreadorDeContenido. \
                validar_registro_creador_de_contenido(creador_de_contenido)
            codigo_error = "es_grupo_no_es_booleano"
            self.assertEqual(codigo_error, errores_creador_de_contenido[0]['error'])

    def test_validar_usuario_ya_tiene_creador_de_contenido(self):
        with self.app.app_context():
            usuario = Usuario(id_usuario=1, nombre_usuario="No lo se", contrasena="123456", tipo_usuario=1,
                              correo_electronico="asd@df.com")
            error_ya_tiene_creador = ValidacionCreadorDeContenido. \
                validar_usuario_tiene_creador_de_contenido_asociado(usuario)
            codigo_error = "usuario_tiene_un_creador_de_contenido_registrado"
            self.assertEqual(codigo_error, error_ya_tiene_creador['error'])

    def test_validar_usuario_no_tiene_creador_de_contenido(self):
        with self.app.app_context():
            usuario = Usuario(id_usuario=3, nombre_usuario="No lo se", contrasena="123456", tipo_usuario=1,
                              correo_electronico="asd@df.com")
            error_ya_tiene_creador = ValidacionCreadorDeContenido. \
                validar_usuario_tiene_creador_de_contenido_asociado(usuario)
            self.assertEqual(None, error_ya_tiene_creador)

    def test_validar_no_existe_creador_de_contenido(self):
        with self.app.app_context():
            existe_creador_de_contenido = ValidacionCreadorDeContenido.validar_existe_creador_de_contenido(2)
            codigo_error = "creador_de_contenido_inexistente"
            self.assertEqual(codigo_error, existe_creador_de_contenido['error'])

    def test_validar_existe_creador_de_contenido(self):
        with self.app.app_context():
            existe_creador_de_contenido = ValidacionCreadorDeContenido.validar_existe_creador_de_contenido(1)
            self.assertEqual(None, existe_creador_de_contenido)

    def test_editar_creador_de_contenido_sin_parametros(self):
        with self.app.app_context():
            creador_de_contenido = CreadorDeContenido(nombre=None, es_grupo=None)
            error_editar = ValidacionCreadorDeContenido.validar_edicion_creador_de_contenido(creador_de_contenido)
            codigo_error = "solicitud_sin_parametros_a_modificar"
            self.assertEqual(codigo_error, error_editar[0]['error'])
