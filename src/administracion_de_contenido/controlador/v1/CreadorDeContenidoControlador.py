from flask_restful import Resource, Api

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido, Artista
from src.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadorDeContenidoControlador(Resource):
    api = Api()

    def get(self, id_creador_contenido):
        """
        Obtiene el creador de contenido que coincide con el id pasado como cadena
        :param id_creador_contenido: El id del creador de contenido que se buscara
        :return: El CreadorDeContenido que coincide con el id o 400 con el error de no existe el creador de contenido
        """
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_existe(id_creador_contenido)
        if error is not None:
            return error, 404
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_contenido)
        return creador_de_contenido.obtener_json()

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador,
                                                       '/v1/creador-de-contenido/<int:id_creador_contenido>')
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
