from flask import jsonify
from flask_restful import Resource, reqparse, Api

from src.manejo_de_usuarios.modelo.Usuario import Usuario, inicializar_base_de_datos
from src.manejo_de_usuarios.util.validaciones.ValidacionUsuario import ValidacionUsuario


class UsuariosControlador(Resource):
    """
    Se encarga de controlar el tipo de peticiones que se le le puede realizar al endpoint
    """
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre_usuario')
        self.parser.add_argument('nombre')
        self.parser.add_argument('contrasena', )
        self.parser.add_argument('tipo_usuario', type=int)
        self.argumentos = self.parser.parse_args(strict=True)

    def get(self):
        """
        Recupera todos los usuarios en la base de datos
        :return: Una lista con todos los usuarios en la base de datos
        """
        usuarios = Usuario.obtener_todos_los_usuario()
        lista_de_usuarios = []
        for usuario in usuarios:
            lista_de_usuarios.append(usuario.obtener_json())
        return jsonify(lista_de_usuarios)

    def post(self):
        """
        Se encarga de agregar un nuevo usuario de tipo ConsumidorDeMusica
        :return:
        """
        self.usuario_a_registrar = Usuario(nombre_usuario=self.argumentos['nombre_usuario'],
                                           nombre=self.argumentos['nombre'], contrasena=self.argumentos['contrasena'],
                                           tipo_usuario=self.argumentos['tipo_usuario'])
        errores_usuario_a_registrar = \
            ValidacionUsuario.validar_usuario_consumidor_de_musica(usuario=self.usuario_a_registrar)
        if len(errores_usuario_a_registrar) > 0:
            errores = {"errores": errores_usuario_a_registrar}
            return errores, 400
        self.usuario_a_registrar.guardar()
        usuario_json = self.usuario_a_registrar.obtener_json()
        return usuario_json

    @staticmethod
    def exponer_endpoint(app):
        """
        Se encarga de exponer el endpoint que manejara la clase
        :param app: Es la app que contiene la instancia de la aplicacion Flask
        :return: None
        """
        UsuariosControlador.api.add_resource(UsuariosControlador, '/usuarios')
        inicializar_base_de_datos(app)
        UsuariosControlador.api.init_app(app)
