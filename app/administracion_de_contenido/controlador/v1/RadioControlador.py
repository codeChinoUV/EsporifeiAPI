from random import sample

from flask_restful import Resource

from app.administracion_de_contenido.modelo.modelos import Cancion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion


class RadioControlador(Resource):

    @token_requerido
    def get(self, usuario_actual, id_cancion):
        """
        Responde una solicitud GET al generar una lista de canciones a partir de la cancion indicada
        :param usuario_actual: El usuario logeado
        :param id_cancion: El id de la cancion de la cual se va a generar la lista de reproduccion
        :return: Una lista de diccionarios o un codigo de error
        """
        validacion_existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if validacion_existe_cancion is not None:
            return validacion_existe_cancion, 404
        radio = Cancion.obtener_estacion_de_readio_a_partir_de_cancion(usuario_actual.id_usuario, id_cancion)
        radio = sample(radio, k=len(radio))
        lista_de_canciones = []
        for cancion in radio:
            lista_de_canciones.append(cancion.obtener_json_con_album())
        return lista_de_canciones, 200
