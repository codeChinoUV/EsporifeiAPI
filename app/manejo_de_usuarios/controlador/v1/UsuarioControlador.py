from flask_restful import Resource, reqparse

from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from app.manejo_de_usuarios.modelo.modelos import Usuario

from app.util.validaciones.modelos.ValidacionUsuario import ValidacionUsuario


class UsuarioControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre_usuario')
        self.parser.add_argument('nombre')
        self.parser.add_argument('contrasena')
        self.parser.add_argument('tipo_usuario')
        self.parser.add_argument('correo_electronico')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    def get(self, usuario_actual):
        """
        Responde a una solicitud de tipo GET regresando la información del usuario logeado
        :param usuario_actual: El usuario logeado
        :return: Un diccionario con la información del usuario logeado
        """
        return usuario_actual.obtener_json(), 200

    def post(self):
        """
        Procesa la informacion de una solicitud POST al agregar un nuevo usuario de tipo ConsumidorDeMusica
        :return: Un diccionario con la informacioón del Usuario registrado o una lista de diccionarios con los errores
        surgidos
        """
        usuario_a_registrar = Usuario(nombre_usuario=self.argumentos['nombre_usuario'],
                                      nombre=self.argumentos['nombre'], contrasena=self.argumentos['contrasena'],
                                      tipo_usuario=self.argumentos['tipo_usuario'],
                                      correo_electronico=self.argumentos['correo_electronico'])
        errores_usuario_a_registrar = \
            ValidacionUsuario.validar_registro_usuario(usuario=usuario_a_registrar)
        if len(errores_usuario_a_registrar) > 0:
            return errores_usuario_a_registrar, 400
        usuario_a_registrar.guardar()
        return usuario_a_registrar.obtener_json()

    @token_requerido
    def patch(self, usuario_actual):
        """
        Procesa una solicitud de tipo PATCH al modificar la informacion del usuario logeado
        :param usuario_actual: El usuario logeado
        :return: La información del usuario modificada o una lista de errores sucedidos
        """
        usuario_modificar = Usuario(nombre_usuario=self.argumentos['nombre_usuario'], nombre=self.argumentos['nombre'],
                                    contrasena=self.argumentos['contrasena'])
        errores = ValidacionUsuario.validar_modificar_usuario(usuario_modificar)
        if errores is not None:
            return errores, 400
        usuario_actual.actualizar_informacion(nombre=usuario_modificar.nombre, contrasena=usuario_modificar.contrasena,
                                              nombre_usuario=usuario_modificar.nombre_usuario,
                                              correo_electronico=usuario_modificar.correo_electronico)
        return usuario_actual.obtener_json(), 202
