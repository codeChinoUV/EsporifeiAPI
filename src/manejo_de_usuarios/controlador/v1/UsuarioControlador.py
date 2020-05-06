from flask_restful import Resource, Api, reqparse

from src.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from src.manejo_de_usuarios.modelo.modelos import Usuario
from src.util.validaciones.ValidacionUsuario import ValidacionUsuario


class UsuarioControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre_usuario')
        self.parser.add_argument('nombre')
        self.parser.add_argument('contrasena')
        self.parser.add_argument('tipo_usuario')
        self.argumentos = self.parser.parse_args(strict=True)

    def post(self):
        """
        Se encarga de agregar un nuevo usuario de tipo ConsumidorDeMusica
        :return:
        """
        usuario_a_registrar = Usuario(nombre_usuario=self.argumentos['nombre_usuario'],
                                      nombre=self.argumentos['nombre'], contrasena=self.argumentos['contrasena'],
                                      tipo_usuario=self.argumentos['tipo_usuario'])
        errores_usuario_a_registrar = \
            ValidacionUsuario.validar_usuario(usuario=usuario_a_registrar)
        if len(errores_usuario_a_registrar) > 0:
            return errores_usuario_a_registrar, 400
        usuario_a_registrar.guardar()
        return usuario_a_registrar.obtener_json()


    @token_requerido
    def get(self, usuario_actual):
        return usuario_actual.obtener_json(), 200

    @staticmethod
    def exponer_endpoint(app):
        UsuarioControlador.api.add_resource(UsuarioControlador, '/v1/usuario')
        UsuarioControlador.api.init_app(app)