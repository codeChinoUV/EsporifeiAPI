from flask import request
from flask_restful import Resource

from app.administracion_de_contenido.modelo.modelos import HistorialCancion, Cancion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido


class HistorialCancionControlador(Resource):

    #def __init__(self):
    #    historialCancion1 = HistorialCancion(id_usuario=3, id_cancion=1)
    #    historialCancion1.guardar_con_fecha(1)
    #    historialCancion2 = HistorialCancion(id_usuario=3, id_cancion=2)
    #    historialCancion2.guardar_con_fecha(8)
    #    historialCancion3 = HistorialCancion(id_usuario=3, id_cancion=3)
    #    historialCancion3.guardar_con_fecha(16)
    #    historialCancion4 = HistorialCancion(id_usuario=3, id_cancion=4)
    #    historialCancion4.guardar_con_fecha(24)
    #    historialCancion5 = HistorialCancion(id_usuario=3, id_cancion=5)
    #    historialCancion5.guardar_con_fecha(32)

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
            if cancion is not None:
                canciones_dicionario.append(cancion_recuperada.obtener_json_con_album())
        return canciones_dicionario, 200


