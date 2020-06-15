from flask_restful import Resource, reqparse

from app.administracion_de_contenido.modelo.modelos import ListaDeReproduccion, Cancion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion
from app.util.validaciones.modelos.ValidacionListaDeReproduccion import ValidacionListaDeReproduccion


class ListasDeReproduccionControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('descripcion')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    def get(self, usuario_actual):
        """
        Se encarga de responder a una solicitud GET al recuperar todas las listas de reproduccion de un usuario
        :param usuario_actual: El usuario del cual se recuperaran las listas de reproduccion
        :return: Un diccionario y un codigo de estado
        """
        listas_de_reproduccion = ListaDeReproduccion. \
            obtener_listas_de_reproduccion_de_usuario(usuario_actual.id_usuario)
        diccionario_de_listas = []
        for lista_de_reproduccion in listas_de_reproduccion:
            diccionario_de_listas.append(lista_de_reproduccion.obtener_json())
        return diccionario_de_listas, 200

    @token_requerido
    def post(self, usuario_actual):
        """
        Se encarga de procesar una solicitud POST al registrar una lista de reproduccion al usuario actual
        :param usuario_actual: El usuario al cual se le registrara la lista de reproduccion
        :return: Un diccionario y un codigo de estado
        """
        lista_de_reproduccion = ListaDeReproduccion(nombre=self.argumentos['nombre'],
                                                    descripcion=self.argumentos['descripcion'])
        errores_validacion = ValidacionListaDeReproduccion.validar_registro_lista_de_reproduccion(lista_de_reproduccion)
        if len(errores_validacion) > 0:
            return errores_validacion, 400
        lista_de_reproduccion.usuario_id = usuario_actual.id_usuario
        lista_de_reproduccion.guardar()
        return lista_de_reproduccion.obtener_json(), 201


class ListaDeReproduccionControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('descripcion')
        self.argumentos = self.parser.parse_args()

    @staticmethod
    def validaciones_existencia_de_lista_y_permisos(usuario_actual, id_lista_de_reproduccion):
        """
        Valida que la cancion exista y que el usuario sea el dueño de la lista de reproduccion
        :param usuario_actual: El usuario que se logeo
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a validar
        :return: Un diccionario y un codigo de estado si ocurrio un error o None si no hay errores
        """
        error_no_existe_cancion = ValidacionListaDeReproduccion. \
            validar_no_existe_lista_de_reproduccion(id_lista_de_reproduccion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion, 404
        error_no_es_dueno = ValidacionListaDeReproduccion. \
            validar_usuario_es_dueno_de_lista_de_reproduccion(id_lista_de_reproduccion, usuario_actual.id_usuario)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403

    def get(self, id_lista_de_reproduccion):
        """
        Se encarga de responder a una solicitud GET al regresar la lista de reproduccion con el id_lista_de_reproduccion
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a obtener
        :return: Un diccionario y un codigo de estado
        """
        error_no_existe_cancion = ValidacionListaDeReproduccion. \
            validar_no_existe_lista_de_reproduccion(id_lista_de_reproduccion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion, 404
        lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(id_lista_de_reproduccion)
        return lista_de_reproduccion.obtener_json(), 200

    @token_requerido
    def patch(self, usuario_actual, id_lista_de_reproduccion):
        """
        Se encarga de procesar una solicitud PATCH al editar la información de la lista de reproduccion
        :param usuario_actual: El usuario logeado
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a editar
        :return: Un diccionario y un codigo de estado
        """
        validaciones_permisos = ListaDeReproduccionControlador. \
            validaciones_existencia_de_lista_y_permisos(usuario_actual, id_lista_de_reproduccion)
        if validaciones_permisos is not None:
            return validaciones_permisos
        lista_de_reproduccion_a_editar = ListaDeReproduccion(nombre=self.argumentos['nombre'],
                                                             descripcion=self.argumentos['descripcion'])
        error_validacion_editar = ValidacionListaDeReproduccion. \
            validar_edicion_lista_de_reproduccion(lista_de_reproduccion_a_editar)
        if len(error_validacion_editar) > 0:
            return error_validacion_editar, 400
        lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(id_lista_de_reproduccion)
        lista_de_reproduccion.editar(nombre=self.argumentos['nombre'], descripcion=self.argumentos['descripcion'])
        return lista_de_reproduccion.obtener_json(), 202

    @token_requerido
    def delete(self, usuario_actual, id_lista_de_reproduccion):
        """
        Se encarga de procesar una solicitud DELETE al eliminar la lista de reproduccion
        :param usuario_actual: El usuario logeado
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a eliminar
        :return: Un diccionario y un codigo de estado
        """
        validaciones_permisos = ListaDeReproduccionControlador. \
            validaciones_existencia_de_lista_y_permisos(usuario_actual, id_lista_de_reproduccion)
        if validaciones_permisos is not None:
            return validaciones_permisos
        lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(id_lista_de_reproduccion)
        lista_de_reproduccion.eliminar()
        return lista_de_reproduccion.obtener_json(), 202


class ListaDeReproduccionCanciones(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    def post(self, usuario_actual, id_lista_de_reproduccion):
        error_no_existe_lista_reproduccion = ValidacionListaDeReproduccion. \
            validar_no_existe_lista_de_reproduccion(id_lista_de_reproduccion)
        if error_no_existe_lista_reproduccion is not None:
            return error_no_existe_lista_reproduccion, 404
        error_no_es_dueno = ValidacionListaDeReproduccion. \
            validar_usuario_es_dueno_de_lista_de_reproduccion(id_lista_de_reproduccion, usuario_actual.id_usuario)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        validacion_agregar = ValidacionListaDeReproduccion.validar_agregar_cancion(self.argumentos['id'])
        if validacion_agregar is not None:
            return validacion_agregar, 400
        cancion = Cancion.obtener_cancion_por_id(self.argumentos['id'])
        lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(id_lista_de_reproduccion)
        lista_de_reproduccion.agregar_cancion(cancion)
        return cancion.obtener_json_con_album(), 201

    def get(self, id_lista_de_reproduccion):
        error_no_existe_lista_reproduccion = ValidacionListaDeReproduccion. \
            validar_no_existe_lista_de_reproduccion(id_lista_de_reproduccion)
        if error_no_existe_lista_reproduccion is not None:
            return error_no_existe_lista_reproduccion, 404
        lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(id_lista_de_reproduccion)
        lista_de_canciones = []
        for cancion in lista_de_reproduccion.canciones:
            lista_de_canciones.append(cancion.obtener_json_con_album())
        return lista_de_canciones, 200


class ListaDeReproduccionCancion(Resource):

    @token_requerido
    def delete(self, usuario_actual, id_lista_de_reproduccion, id_cancion):
        """
        Se encarga de procesar una solicitud DELETE al eliminar la cancion con el id_cancion en la lista de reproduccion
        con el id_lista_de_reproduccion
        :param usuario_actual: El usuario logeado
        :param id_cancion: El id de la cancion a quitar de la lista de reproduccion
        :param id_lista_de_reproduccion: La lista de reproduccion de la cual se eliminara la cancion
        :return: Un diccionario y un codigo de estado
        """
        error_no_existe_lista_reproduccion = ValidacionListaDeReproduccion. \
            validar_no_existe_lista_de_reproduccion(id_lista_de_reproduccion)
        if error_no_existe_lista_reproduccion is not None:
            return error_no_existe_lista_reproduccion, 404
        error_no_es_dueno = ValidacionListaDeReproduccion. \
            validar_usuario_es_dueno_de_lista_de_reproduccion(id_lista_de_reproduccion, usuario_actual.id_usuario)
        if error_no_es_dueno is not None:
            return error_no_es_dueno, 403
        error_cancion_no_en_lista = ValidacionListaDeReproduccion. \
            validar_existe_cancion_en_lista_de_reproduccion(id_lista_de_reproduccion, id_cancion)
        if error_cancion_no_en_lista is not None:
            return error_cancion_no_en_lista, 404
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        lista_de_reproduccion = ListaDeReproduccion.obtener_lista_de_reproduccion(id_lista_de_reproduccion)
        lista_de_reproduccion.quitar_cancion(cancion)
        return cancion.obtener_json_con_album(), 202
