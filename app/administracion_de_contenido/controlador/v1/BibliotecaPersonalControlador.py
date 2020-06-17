from flask import request
from flask_restful import Resource, reqparse

from app.administracion_de_contenido.modelo.modelos import CancionPersonal
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from app.util.validaciones.modelos.ValidacionCancionPersonal import ValidacionCancionPersonal


class BibliotecaPersonalCanciones(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('album')
        self.parser.add_argument('artistas')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    def post(self, usuario_actual):
        """
        Se encarga de procesar una solicitud POST al registrar una cancionPersonal de un usuario
        :param usuario_actual: El usuario que se encuentra logeado
        :return: Un diccionario y un codigo de estado
        """
        cancion_a_registrar = CancionPersonal(nombre=self.argumentos['nombre'], artistas=self.argumentos['artistas'],
                                              album=self.argumentos['album'], id_usuario=usuario_actual.id_usuario)
        errores_validacion_registro = ValidacionCancionPersonal.validar_registro_cancion_personal(cancion_a_registrar)
        if errores_validacion_registro is not None:
            return errores_validacion_registro, 400
        cancion_a_registrar.guardar()
        return cancion_a_registrar.obtener_json(), 201

    @token_requerido
    def get(self, usuario_actual):
        """
        Se encarga de procesar una solicitud GET al devolver las canciones del usuario
        :param usuario_actual: El usuario logead
        :return: Una lista de dicionanrios y un codigo de estado
        """
        cantidad = request.args.get('cantidad')
        pagina = request.args.get('pagina')
        try:
            if cantidad is not None and pagina is not None:
                cantidad = int(cantidad)
                pagina = int(pagina)
            else:
                cantidad = 10
                pagina = 1
            canciones = CancionPersonal.obtener_canciones_de_usuario(usuario_actual.id_usuario, cantidad, pagina)
        except ValueError:
            canciones = CancionPersonal.obtener_canciones_de_usuario(usuario_actual.id_usuario)
        lista_canciones = []
        for cancion in canciones:
            lista_canciones.append(cancion.obtener_json())
        return lista_canciones, 200
