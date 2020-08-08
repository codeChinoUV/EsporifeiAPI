import os

from flask import request
from flask_restful import Resource

from app import create_app
from app.administracion_de_contenido.modelo.modelos import HistorialCancion, Cancion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido

settings_module = os.getenv('APP_SETTINGS_MODULE')

class HistorialCancionControlador(Resource):

    @token_requerido
    def get(self, usuario_actual):
        """
        Se encarga de procesar una solicitud GET al devolver las canciones que ha reproducido el usuario actual
        :param usuario_actual: El usuario logeado
        :return: Una lista de diccionarios y un codigo de estado
        """
        cantidad = request.args.get('cantidad')
        pagina = request.args.get('pagina')
        ultimos_dias_a_obtener = request.args.get('ultimos_dias_a_obtener')
        try:
            if cantidad is not None and pagina is not None and ultimos_dias_a_obtener is not None:
                cantidad = int(cantidad)
                pagina = int(pagina)
                ultimos_dias_a_obtener = int(ultimos_dias_a_obtener)
            else:
                cantidad = 10
                pagina = 1
                ultimos_dias_a_obtener = 7
            canciones = HistorialCancion.obtener_canciones_de_usuario(usuario_actual.id_usuario, cantidad, pagina,
                                                                      ultimos_dias_a_obtener)
        except ValueError:
            canciones = HistorialCancion.obtener_canciones_de_usuario(usuario_actual.id_usuario)
        canciones_dicionario = []
        for cancion in canciones:
            cancion_recuperada = Cancion.obtener_cancion_por_id(cancion.id_cancion)
            if cancion_recuperada is not None:
                canciones_dicionario.append(cancion_recuperada.obtener_json_con_album())
        return canciones_dicionario, 200

    @staticmethod
    def agregar_cancion_a_historial_usuario(id_usuario, id_cancion):
        """
        Agrega al historial del usuario con el id_usuario la cancion con el id_cancion
        :param id_usuario: El id del usuario al que se le agregara la cancion a su historial
        :param id_cancion: La cancion a agregar al historial
        :return: None
        """
        app = create_app(settings_module)
        with app.app_context():
            historial = HistorialCancion(id_usuario=id_usuario, id_cancion=id_cancion)
            historial.guardar()
