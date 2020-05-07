from flask_restful import Resource, Api, reqparse

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido, Artista
from src.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido, solo_creador_de_contenido
from src.util.JsonBool import JsonBool
from src.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadorDeContenidoControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('biografia')
        self.parser.add_argument('es_grupo')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual):
        """
        Obtiene el creador de contenido del usuario_actual
        :return: El CreadorDeContenido del usuario o un diccionario con el error
        """
        error = ValidacionCreadorDeContenido.validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error is not None:
            return error, 404
        creador_de_contenido = CreadorDeContenido. \
            obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        return creador_de_contenido.obtener_json()

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        """
        Se encarga de registrar un nuevo creador de contenido
        :return: Una lista de errores de los errores en la solictud o un diccionario con los datos del creador de
        contenido registrado
        """
        creador_de_contenido_a_registrar = CreadorDeContenido(nombre=self.argumentos['nombre'],
                                                              biografia=self.argumentos['biografia'],
                                                              es_grupo=self.argumentos['es_grupo'],
                                                              usuario_nombre_usuario=usuario_actual.nombre_usuario)
        error_creador_ya_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_ya_registrado is not None:
            return error_creador_ya_registrado, 400
        errores_en_la_solicitid = \
            ValidacionCreadorDeContenido.validar_registro_creador_de_contenido(creador_de_contenido_a_registrar)
        if len(errores_en_la_solicitid) > 0:
            return errores_en_la_solicitid, 400
        creador_de_contenido_a_registrar.es_grupo = JsonBool \
            .obtener_boolean_de_valor_json(creador_de_contenido_a_registrar.es_grupo)
        creador_de_contenido_a_registrar.guardar()
        return creador_de_contenido_a_registrar.obtener_json(), 201

    @token_requerido
    @solo_creador_de_contenido
    def put(self, usuario_actual):
        """
        Se encarga de responder a las peticiones de tipo put, su funcion es editar la información de un creador de
        contenido
        :return: Un JSON con la informacion del objeto editada y un codigo de respuesta 202 o un JSON con una lista de
         errores y un codigo de respuesta 400
        """
        error_creador_no_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_no_registrado is not None:
            return error_creador_no_registrado, 400

        creador_de_contenido_a_validar = CreadorDeContenido(nombre=self.argumentos['nombre'],
                                                            biografia=self.argumentos['biografia'],
                                                            es_grupo=self.argumentos['es_grupo'])

        errores_en_la_solicitud = ValidacionCreadorDeContenido \
            .validar_edicion_creador_de_contenido(creador_de_contenido_a_validar)
        if len(errores_en_la_solicitud) > 0:
            return errores_en_la_solicitud, 400

        creador_de_contenido = CreadorDeContenido. \
            obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)

        creador_de_contenido.actualizar_informacion(creador_de_contenido_a_validar.nombre,
                                                    creador_de_contenido_a_validar.biografia,
                                                    creador_de_contenido_a_validar.es_grupo)

        return creador_de_contenido.obtener_json(), 202

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador,
                                                       '/v1/creador-de-contenido')
        CreadorDeContenidoControlador.api.init_app(app)


class ArtistasControlador(Resource):
    api = Api()

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual):
        """
        Contesta una solicitud de tipo GET con una lista de artistas o un diccionario con errores
        :param id_creador_contenido: El id del creador de contenido del cual se recuperaran sus artistas
        """
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_existe(usuario_actual)
        if error is not None:
            return error, 404
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_es_grupo(usuario_actual)
        if error is not None:
            return error, 404
        creador_de_contenido = CreadorDeContenido\
            .obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        artistas_del_creador_de_contenido =\
            Artista.obtener_artistas_de_creador_de_contenido(creador_de_contenido.id_creador_de_contenido)
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
