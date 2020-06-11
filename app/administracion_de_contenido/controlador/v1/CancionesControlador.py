from flask_restful import reqparse, Resource

from app.administracion_de_contenido.modelo.modelos import Album, Cancion, CreadorDeContenido
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido, solo_creador_de_contenido
from app.util.validaciones.modelos.ValidacionAlbum import ValidacionAlbum
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadorDeContenidoAlbumCanciones(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual, id_album):
        error_creador_no_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_no_registrado is not None:
            return error_creador_no_registrado, 400
        error_no_existe_album = ValidacionAlbum.validar_album_existe(id_album)
        if error_no_existe_album is not None:
            return error_no_existe_album, 404
        error_no_es_dueno = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario,
                                                                                           id_album)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        album = Album.obtener_album_por_id(id_album)
        canciones = []
        for cancion in album.canciones:
            if not cancion.eliminada:
                canciones.append(cancion.obtener_json_con_creadores())
        return canciones, 200

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual, id_album):
        error_creador_no_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_no_registrado is not None:
            return error_creador_no_registrado, 400
        error_no_existe_album = ValidacionAlbum.validar_album_existe(id_album)
        if error_no_existe_album is not None:
            return error_no_existe_album, 404
        error_no_es_dueno = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario,
                                                                                           id_album)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        cancion = Cancion(nombre=self.argumentos['nombre'])
        error_registro_cancion = ValidacionCancion.validar_registro_cancion(cancion)
        if error_registro_cancion is not None:
            return error_registro_cancion, 400
        album = Album.obtener_album_por_id(id_album)
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        album.agregar_cancion(cancion, creador_de_contenido)
        return cancion.obtener_json_con_creadores(), 201


class CreadorDeContenidoAlbumCancion(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.argumentos = self.parser.parse_args(strict=True)

    @staticmethod
    def validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion):
        error_creador_no_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_no_registrado is not None:
            return error_creador_no_registrado, 400
        error_no_existe_album = ValidacionAlbum.validar_album_existe(id_album)
        if error_no_existe_album is not None:
            return error_no_existe_album, 404
        no_es_dueno_album = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario,
                                                                                           id_album)
        if no_es_dueno_album is not None:
            return no_es_dueno_album, 403
        no_existe_cancion = ValidacionCancion.validar_no_existe_cancion(id_album, id_cancion)
        if no_existe_cancion is not None:
            return no_existe_cancion, 404
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        no_es_dueno_de_cancion = ValidacionCancion. \
            validar_creador_de_contenido_es_dueno_de_cancion(id_cancion, creador_de_contenido.id_creador_de_contenido)
        if no_es_dueno_de_cancion is not None:
            return no_es_dueno_de_cancion, 403

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual, id_album, id_cancion):
        CreadorDeContenidoAlbumCancion.validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        return cancion.obtener_json_con_creadores(), 200

    @token_requerido
    @solo_creador_de_contenido
    def patch(self, usuario_actual, id_album, id_cancion):
        error_permisos = CreadorDeContenidoAlbumCancion.\
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if error_permisos is not None:
            return error_permisos
        cancion_a_editar = Cancion(nombre=self.argumentos['nombre'])
        validacion = ValidacionCancion.validar_registro_cancion(cancion_a_editar)
        if validacion is not None:
            return validacion
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cancion.editar(cancion_a_editar.nombre)
        return cancion.obtener_json_con_creadores(), 202

    @token_requerido
    @solo_creador_de_contenido
    def delete(self, usuario_actual, id_album, id_cancion):
        error_permisos = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if error_permisos is not None:
            return error_permisos
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cancion.eliminar()
        return cancion.obtener_json_con_creadores(), 202
