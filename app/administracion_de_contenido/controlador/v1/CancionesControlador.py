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
        cancion = Cancion(nombre=self.argumentos['nombre'])
        error_no_es_dueno = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario,
                                                                                           id_album)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        error_registro_cancion = ValidacionCancion.validar_registro_cancion(cancion)
        if error_registro_cancion is not None:
            return error_registro_cancion, 400
        album = Album.obtener_album_por_id(id_album)
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        album.agregar_cancion(cancion, creador_de_contenido)
        return cancion.obtener_json_con_creadores(), 201
