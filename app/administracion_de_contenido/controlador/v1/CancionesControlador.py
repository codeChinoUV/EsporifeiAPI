import os

from flask import request
from flask_restful import reqparse, Resource

from app import create_app
from app.administracion_de_contenido.modelo.modelos import Album, Cancion, CreadorDeContenido, Genero, HistorialCancion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido, solo_creador_de_contenido
from app.util.validaciones.modelos.ValidacionAlbum import ValidacionAlbum
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from app.util.validaciones.modelos.ValidacionGenero import ValidacionGenero

settings_module = os.getenv('APP_SETTINGS_MODULE')

class CreadorDeContenidoAlbumCanciones(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual, id_album):
        """
        Responde una solictud GET al devolver todas las canciones del Albm
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album a recuperar las canciones
        :return: Un diccionario y un codigo de estado
        """
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
        """
        Procesa una solicitud POST al registrar una nueva cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El album en donde se va a registrar la cancion
        :return: Un diccionario y un codigo de error
        """
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
        self.argumentos = self.parser.parse_args()

    @staticmethod
    def validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion):
        """
        Se encarga de validar que el alum y la cancion existen, se encarga validar que el usuario es propietario del
        album y cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album a validar
        :param id_cancion: El id de la cancion a validar si existe
        :return: Un diccionario y un codigo de estado
        """
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
        """
        Se encarga de procesar una solicitud GET al devolver la cancion con el id_cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertence la cancion
        :param id_cancion: El id de la cancion a recuperar
        :return: Un diccionario y un codigo de estado
        """
        error_permisos = CreadorDeContenidoAlbumCancion \
            .validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if error_permisos is not None:
            return error_permisos
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        return cancion.obtener_json_con_creadores(), 200

    @token_requerido
    @solo_creador_de_contenido
    def put(self, usuario_actual, id_album, id_cancion):
        """
        Se encarga de procesar una solictud PATCH al editar la informacion de la cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertenece la cancion
        :param id_cancion: El id de la cancion a editar
        :return: Un diccionario y un codigo de estado
        """
        error_permisos = CreadorDeContenidoAlbumCancion. \
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
        """
        Se encarga de procesar una solicitud de tipo DELETE
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertence la cancion
        :param id_cancion: El id de la cancion a eliminar
        :return: Un diccionario y un codigo de estado
        """
        error_permisos = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if error_permisos is not None:
            return error_permisos
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cancion.eliminar()
        return cancion.obtener_json_con_creadores(), 202

    @staticmethod
    def modificar_duracion(id_cancion, duracion_total):
        app = create_app(settings_module)
        with app.app_context():
            Cancion.modificar_duracion(id_cancion, duracion_total)


class CreadorDeContenidoAlbumCancionGeneros(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual, id_album, id_cancion):
        """
        Se encarga de procesar una solicitud POST al agregar un genero a la cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertenece la cancion
        :param id_cancion: El id de la cancion a la cual se le agregara el genero
        :return: Un diccionario y un codigo de estado
        """
        errores_permiso = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if errores_permiso is not None:
            return errores_permiso
        error_id_genero = ValidacionGenero.validar_agregar_genero(self.argumentos['id'])
        if error_id_genero is not None:
            return error_id_genero, 400
        genero = Genero.obtener_genero_por_id(self.argumentos['id'])
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cancion.agregar_genero(genero)
        return genero.obtener_json(), 201

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual, id_album, id_cancion):
        """
        Se encarga de procesar una solicitud POST al devolver los generos de una cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertence la cancion
        :param id_cancion: El id de la cancion de la cual se recuperaran los generos
        :return: Un diccionario y un codigo de estado
        """
        errores_permiso = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if errores_permiso is not None:
            return errores_permiso
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        generos = []
        for genero in cancion.generos:
            generos.append(genero.obtener_json())
        return generos, 200


class CreadorDeContenidoAlbumCancionGenero(Resource):

    @token_requerido
    @solo_creador_de_contenido
    def delete(self, usuario_actual, id_album, id_cancion, id_genero):
        """
        Se encarga de responder a una solicitud DELETE a eliminar un Genero de la lista de Generos de la Cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertenece la cancion
        :param id_cancion: El id de la cancion a eliminar el genero
        :param id_genero: El id del genero a quitar de la cancion
        :return: Un diccionario y un codigo de estado
        """
        errores_permiso = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if errores_permiso is not None:
            return errores_permiso
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        error_no_tiene_genero = ValidacionCancion.validar_tiene_genero(cancion, id_genero)
        if error_no_tiene_genero is not None:
            return error_no_tiene_genero, 404
        genero = Genero.obtener_genero_por_id(id_genero)
        cancion.eliminar_genero(genero)
        return genero.obtener_json(), 202


class CreadoresDeContenidoAlbumesCanciones(Resource):

    def get(self, id_creador_de_contenido, id_album):
        """
        Se encarga de procesar una solicitud GET al devolver las canciones del album del creador de contenido
        :param id_album: El id del album a recuperar las canciones
        :param id_creador_de_contenido: El id del creador de contenido a recuperar las canciones
        :return: Un diccionario y un codigo de estado
        """
        error_creador_no_existe = ValidacionCreadorDeContenido. \
            validar_existe_creador_de_contenido(id_creador_de_contenido)
        if error_creador_no_existe is not None:
            return error_creador_no_existe, 404
        error_album_no_existe = ValidacionAlbum.validar_creador_de_contenido_tiene_album(id_creador_de_contenido,
                                                                                         id_album)
        if error_album_no_existe is not None:
            return error_album_no_existe, 404
        canciones = []
        album = Album.obtener_album_por_id(id_album)
        for cancion in album.canciones:
            if not cancion.eliminada:
                canciones.append(cancion.obtener_json_con_creadores())
        return canciones, 200


class CreadorDeContenidoAlbumesCancionCreadoresDeContenidoControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual, id_album, id_cancion):
        """
        Se encarga de procesar una solicitud de tipo POST al agregar un creador de contenido a la cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al que pertence la cancion
        :param id_cancion: El id de la cancion a la que se le agregara el creador de contenido
        :return: Un diccionario y un codigo de estado
        """
        errores_permiso = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if errores_permiso is not None:
            return errores_permiso
        errores_validacion_id = ValidacionCreadorDeContenido.validar_agregar_creador_de_contenido(self.argumentos['id'])
        if errores_validacion_id is not None:
            return errores_validacion_id, 400
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(self.argumentos['id'])
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        cancion.agregar_creador_de_contenido(creador_de_contenido)
        return creador_de_contenido.obtener_json_sin_genero(), 201


class CreadorDeContenidoAlbumesCancionCreadorDeContenidoControlador(Resource):

    @token_requerido
    @solo_creador_de_contenido
    def delete(self, usuario_actual, id_album, id_cancion, id_creador_contenido):
        """
        Se encarga de responder a una solicitud DELETE a eliminar un creador de contenido
         de la lista de creadores de contenido de la Cancion
        :param usuario_actual: El usuario logeado
        :param id_album: El id del album al cual pertenece la cancion
        :param id_cancion: El id de la cancion a eliminar el creador de la cancion
        :param id_creador_contenido: El id del creador de contenido a quitar
        :return: Un diccionario y un codigo de estado
        """
        errores_permiso = CreadorDeContenidoAlbumCancion. \
            validaciones_de_acceso_y_existencia(usuario_actual, id_album, id_cancion)
        if errores_permiso is not None:
            return errores_permiso
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        error_no_tiene_creador_contenido = ValidacionCancion.validar_tiene_creador_de_contenido(cancion,
                                                                                                id_creador_contenido)
        if error_no_tiene_creador_contenido is not None:
            return error_no_tiene_creador_contenido, 404
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_contenido)
        cancion.eliminar_creador_de_contenido(creador_de_contenido)
        return creador_de_contenido.obtener_json(), 202


class CancionesBucarControlador(Resource):

    def get(self, cadena_busqueda):
        """
        Se encarga de responder a una solicitud de tipo GET al devolver las canciones que coincidan con la cadena de
        busqueda
        :param cadena_busqueda: La cadena de busqueda
        :return: Un diccionario y en codigo de estado
        """
        cantidad = request.args.get('cantidad')
        pagina = request.args.get('pagina')
        try:
            if cantidad is not None and pagina is not None:
                cantidad = int(cantidad)
                pagina = int(pagina)
            else:
                cantidad = 10
                pagina = 1
            canciones = Cancion.obtener_canciones_por_busqueda(cadena_busqueda, cantidad, pagina)
        except ValueError:
            canciones = Cancion.obtener_canciones_por_busqueda(cadena_busqueda)
        canciones_dicionario = []
        for cancion in canciones:
            canciones_dicionario.append(cancion.obtener_json_con_album())
        return canciones_dicionario, 200
