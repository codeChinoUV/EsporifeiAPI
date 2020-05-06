from flask_restful import Resource, Api

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido, Artista
from src.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from src.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from src.util.validaciones.modelos.ValidacionUsuario import ValidacionUsuario


class CreadorDeContenidoControlador(Resource):
    api = Api()

    @token_requerido
    def get(self, usuario_actual):
        """
        Obtiene el creador de contenido del usuario_actual
        :return: El CreadorDeContenido del usuario o un diccionario con el error
        """
        error = ValidacionUsuario.validar_tipo_usuario_creador_de_contenido(usuario_actual)
        if error is not None:
            return error, 404
        error = ValidacionCreadorDeContenido.validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error is not None:
            return error, 404
        creador_de_contenido = CreadorDeContenido.\
            obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        return creador_de_contenido.obtener_json()
    

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador,
                                                       '/v1/creador-de-contenido')
        CreadorDeContenidoControlador.api.init_app(app)


class ArtistasControlador(Resource):
    api = Api()

    def get(self, id_creador_contenido):
        """
        Contesta una solicitud de tipo GET con una lista de artistas o un diccionario con errores
        :param id_creador_contenido: El id del creador de contenido del cual se recuperaran sus artistas
        """
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_existe(id_creador_contenido)
        if error is not None:
            return error, 404
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_es_grupo(id_creador_contenido)
        if error is not None:
            return error, 404
        artistas_del_creador_de_contenido = Artista.obtener_artistas_de_creador_de_contenido(id_creador_contenido)
        diccionario_de_artistas = []
        for artista in artistas_del_creador_de_contenido:
            diccionario_de_artistas.append(artista.obtener_json())
        return diccionario_de_artistas

    @staticmethod
    def exponer_end_point(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        ArtistasControlador.api.add_resource(ArtistasControlador,
                                             '/v1/creador-de-contenido/<int:id_creador_contenido>/artistas')
        ArtistasControlador.api.init_app(app)
