from flask_restful import Resource, Api, reqparse

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido, Artista
from src.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido, solo_creador_de_contenido
from src.util.JsonBool import JsonBool
from src.util.validaciones.modelos.ValidacionArtista import ValidacionArtista
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
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador,
                                                       '/v1/creador-de-contenido')
        CreadorDeContenidoControlador.api.init_app(app)


class ArtistasControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual):
        """
        Contesta una solicitud de tipo GET con una lista de artistas o un diccionario con errores
        :param usuario_actual: El usuario actual con el que se autentico
        :return: Los artistas que tiene registrado un CreadorDeContenido
        """
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_existe_a_partir_de_usuario(usuario_actual)
        if error is not None:
            return error, 404
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_es_grupo_a_partir_de_usuario(usuario_actual)
        if error is not None:
            return error, 404
        creador_de_contenido = CreadorDeContenido \
            .obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        artistas_del_creador_de_contenido = \
            Artista.obtener_artistas_de_creador_de_contenido(creador_de_contenido.id_creador_de_contenido)
        diccionario_de_artistas = []
        for artista in artistas_del_creador_de_contenido:
            diccionario_de_artistas.append(artista.obtener_json())
        return diccionario_de_artistas

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        """
        Se encarga de procesar una solictud POST al registrar un nuevo artista de un creador de contenido que es grupo
        """
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_existe_a_partir_de_usuario(usuario_actual)
        if error is not None:
            return error, 404
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_es_grupo_a_partir_de_usuario(usuario_actual)
        if error is not None:
            return error, 404
        artista_a_registrar = Artista(nombre=self.argumentos['nombre'])
        errores_en_la_solicitud = ValidacionArtista.validar_artista(artista_a_registrar)
        if len(errores_en_la_solicitud) > 0:
            return errores_en_la_solicitud, 400
        creador_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        artista_a_registrar.creador_de_contenido_id = creador_contenido.id_creador_de_contenido
        artista_a_registrar.guardar()
        return artista_a_registrar.obtener_json(), 201

    @staticmethod
    def exponer_end_point(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        ArtistasControlador.api.add_resource(ArtistasControlador,
                                             '/v1/creador-de-contenido/artistas')
        ArtistasControlador.api.init_app(app)


class ArtistaControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual, id_artista):
        """
        Se encarga de responder a una solictud GET con la informacion del Artista o con una lista de los errores
        ocurridos y su codigo
        """
        error_no_existe_artista = ValidacionArtista.validar_artista_existe(id_artista)
        if error_no_existe_artista is not None:
            return error_no_existe_artista, 404
        creador_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        error_no_es_dueno = ValidacionArtista \
            .validar_usuario_es_dueno_de_artista(creador_contenido.id_creador_de_contenido, id_artista)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        artista = Artista.obtener_artista_por_id(id_artista)
        return artista.obtener_json()

    @token_requerido
    @solo_creador_de_contenido
    def put(self, usuario_actual, id_artista):
        """
        Se encarga de procesar a una solicitud PUT al modificar la informacion de un Artista
        """
        error_no_existe_artista = ValidacionArtista.validar_artista_existe(id_artista)
        if error_no_existe_artista is not None:
            return error_no_existe_artista, 404
        creador_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        error_no_es_dueno = ValidacionArtista \
            .validar_usuario_es_dueno_de_artista(creador_contenido.id_creador_de_contenido, id_artista)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        artista_a_validar = Artista(nombre=self.argumentos['nombre'])
        errores_en_la_solicitud = ValidacionArtista.validar_artista(artista_a_validar)
        if len(errores_en_la_solicitud) > 0:
            return errores_en_la_solicitud, 400
        artista_a_modificar = Artista.obtener_artista_por_id(id_artista)
        artista_a_modificar.actualizar_informacion(artista_a_validar.nombre)
        return artista_a_modificar.obtener_json(), 202

    @token_requerido
    @solo_creador_de_contenido
    def delete(self, usuario_actual, id_artista):
        """
        Se encarga de procesar una solicitud DELETE al eliminar el artista con el id indicado
        """
        error_no_existe_artista = ValidacionArtista.validar_artista_existe(id_artista)
        if error_no_existe_artista is not None:
            return error_no_existe_artista, 404
        creador_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario)
        error_no_es_dueno = ValidacionArtista \
            .validar_usuario_es_dueno_de_artista(creador_contenido.id_creador_de_contenido, id_artista)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        artista_a_eliminar = Artista.obtener_artista_por_id(id_artista)
        artista_a_eliminar.eliminar()
        return artista_a_eliminar.obtener_json(), 202

    @staticmethod
    def exponer_endpoint(app):
        """
        Se encarga de exponer los metodos del endpoint en la app
        :param app: La app en donde se expondran los metodos y el endpoint
        """
        ArtistaControlador.api.add_resource(ArtistaControlador, '/v1/creador-de-contenido/artista/<int:id_artista>')
        ArtistaControlador.api.init_app(app)


class CreadorDeContenidoPublicoControlador(Resource):
    api = Api()

    def get(self, id_creador_de_contenido):
        """
        Se encarga de responder a una solicitud GET con la infomracion del creador que conentenga el
        id_creador_de_conenido
        """
        error_no_existe_creador_de_contenido = ValidacionCreadorDeContenido. \
            validar_existe_creador_de_contenido(id_creador_de_contenido)
        if error_no_existe_creador_de_contenido is not None:
            return error_no_existe_creador_de_contenido, 404
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_de_contenido)
        return creador_de_contenido.obtener_json(), 200

    @staticmethod
    def exponer_endpoint(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        CreadorDeContenidoPublicoControlador.api.add_resource(CreadorDeContenidoPublicoControlador,
                                                              '/v1/creador-de-contenido/<int:id_creador_de_contenido>')
        CreadorDeContenidoPublicoControlador.api.init_app(app)


class ArtistasPublicoControlador(Resource):
    api = Api()

    def get(self, id_creador_de_contenido):
        """
        Responde a una solicitud GET con los artistas que peterncen al CreadorDeContenido con el id indicado
        """
        error = ValidacionCreadorDeContenido.validar_existe_creador_de_contenido(id_creador_de_contenido)
        if error is not None:
            return error, 404
        error = ValidacionCreadorDeContenido.validar_creador_de_contenido_es_grupo(id_creador_de_contenido)
        if error is not None:
            return error, 404
        artistas_del_creador_de_cotenido = Artista.obtener_artistas_de_creador_de_contenido(id_creador_de_contenido)
        lista_de_artistas = []
        for artista in artistas_del_creador_de_cotenido:
            lista_de_artistas.append(artista.obtener_json())
        return lista_de_artistas

    @staticmethod
    def exponer_endpoint(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        ArtistasPublicoControlador.api.add_resource(ArtistasPublicoControlador,
                                                    '/v1/creador-de-contenido/<int:id_creador_de_contenido>/artistas')
        ArtistasPublicoControlador.api.init_app(app)
