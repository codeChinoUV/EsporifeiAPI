from flask_restful import Resource, reqparse

from app.administracion_de_contenido.modelo.modelos import Album, CreadorDeContenido
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido, solo_creador_de_contenido
from app.util.validaciones.modelos.ValidacionAlbum import ValidacionAlbum
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadorDeContenidoAlbumes(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('anio_lanzamiento')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        error_no_existe_creador_cotenido = ValidacionCreadorDeContenido \
            .validar_creador_de_contenido_existe_a_partir_de_usuario(usuario_actual)
        if error_no_existe_creador_cotenido is not None:
            return error_no_existe_creador_cotenido, 404
        album_a_registrar = Album(nombre=self.argumentos['nombre'],
                                  anio_lanzamiento=self.argumentos['anio_lanzamiento'])
        errores_validaciones = ValidacionAlbum.validar_registro_album(album_a_registrar)
        if len(errores_validaciones) > 0:
            return errores_validaciones, 400
        album_a_registrar.creador_de_contenido_id = CreadorDeContenido \
            .obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario).id_creador_de_contenido
        album_a_registrar.guardar()
        return album_a_registrar.obtener_json(), 201

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual):
        error_no_existe_creador_cotenido = ValidacionCreadorDeContenido \
            .validar_creador_de_contenido_existe_a_partir_de_usuario(usuario_actual)
        if error_no_existe_creador_cotenido is not None:
            return error_no_existe_creador_cotenido, 404
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(
            usuario_actual.id_usuario)
        albumes = Album.obtener_abumes_creador_de_contenido(creador_de_contenido.id_creador_de_contenido)
        lista_de_albumes = []
        for album in albumes:
            lista_de_albumes.append(album.obtener_json())
        return lista_de_albumes, 200


class CreadorDeContenidoAlbum(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('anio_lanzamiento')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual, id_album):
        """
        Se encarga de responder a una solictud GET con la informacion del Álbum o con una lista de los errores
        ocurridos y su código
        """
        creador_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        album = Album.obtener_album_por_id(id_album)
        if album is None:
            return None, 404
        return album.obtener_json()

    @token_requerido
    @solo_creador_de_contenido
    def delete(self, usuario_actual, id_album):
        """
        Se encarga de procesar a una solicitud PUT al modificar la información de un Álbum y simular
        su eliminación
        """
        error_no_existe_album = ValidacionAlbum.validar_album_existe(id_album)
        if error_no_existe_album is not None:
            return error_no_existe_album, 404
        error_no_es_dueno = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario,
                                                                                           id_album)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        album_a_modificar = Album.obtener_album_por_id(id_album)
        album_a_modificar.eliminar_informacion()
        return album_a_modificar.obtener_json(), 202

    @token_requerido
    @solo_creador_de_contenido
    def put(self, usuario_actual, id_album):
        """
        Se encarga de procesar a una solicitud PATCH al modificar la información de un Álbum
        """
        error_no_existe_album = ValidacionAlbum.validar_album_existe(id_album)
        if error_no_existe_album is not None:
            return error_no_existe_album, 404
        error_no_es_dueno = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario,
                                                                                           id_album)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        album_a_validar = Album(nombre=self.argumentos['nombre'],
                                anio_lanzamiento=self.argumentos['anio_lanzamiento'])
        errores_validaciones = ValidacionAlbum.validar_registro_album(album_a_validar)
        if len(errores_validaciones) > 0:
            return errores_validaciones, 400
        album_a_modificar = Album.obtener_album_por_id(id_album)
        album_a_modificar.actualizar_informacion(album_a_validar.nombre, album_a_validar.anio_lanzamiento)
        return album_a_modificar.obtener_json(), 202


class AlbumesPublicoControlador(Resource):

    def get(self, id_creador_de_contenido):
        """
        Responde a una solicitud GET con los álbumes que peternecen al CreadorDeContenido con el id indicado
        """
        error = ValidacionAlbum.validar_existe_creador_de_contenido(id_creador_de_contenido)
        if error is not None:
            return error, 404
        albumes_del_creador_de_contenido = Album.obtener_abumes_creador_de_contenido(id_creador_de_contenido)
        lista_de_albumes = []
        for album in albumes_del_creador_de_contenido:
            lista_de_albumes.append(album.obtener_json())
        return lista_de_albumes


class AlbumBuscarControlador(Resource):
    def get(self, cadena_busqueda):
        """
        Se encarga de responder una peticion GET al buscar todos los álbumes que coincidan
        con la cadena de busqueda
        :param cadena_busqueda: La cadena de busqueda que se utlizara para filtrar los álbumes
        """
        albumes = Album.obtener_album_por_busqueda(cadena_busqueda)
        albumes_diccionario = []
        if len(albumes) > 0:
            for album in albumes:
                albumes_diccionario.append(album.obtener_json())
        return albumes_diccionario
