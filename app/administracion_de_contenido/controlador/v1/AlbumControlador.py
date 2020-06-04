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
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        error_no_existe_creador_cotenido = ValidacionCreadorDeContenido\
            .validar_creador_de_contenido_existe_a_partir_de_usuario(usuario_actual)
        if error_no_existe_creador_cotenido is not None:
            return error_no_existe_creador_cotenido, 404
        album_a_registrar = Album(nombre=self.argumentos['nombre'],
                                  anio_lanzamiento=self.argumentos['anio_lanzamiento'])
        errores_validaciones = ValidacionAlbum.validar_registro_album(album_a_registrar)
        if len(errores_validaciones) > 0:
            return errores_validaciones, 400
        album_a_registrar.creador_de_contenido_id = CreadorDeContenido\
            .obtener_creador_de_contenido_por_usuario(usuario_actual.nombre_usuario).id_creador_de_contenido
        album_a_registrar.guardar()
        return album_a_registrar.obtener_json(), 201

