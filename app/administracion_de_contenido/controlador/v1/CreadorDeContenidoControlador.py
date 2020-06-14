from flask import request
from flask_restful import Resource, reqparse

from app.administracion_de_contenido.modelo.modelos import CreadorDeContenido, Genero
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido, solo_creador_de_contenido
from app.util.JsonBool import JsonBool
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from app.util.validaciones.modelos.ValidacionGenero import ValidacionGenero


class CreadorDeContenidoControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('biografia')
        self.parser.add_argument('es_grupo')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def get(self, usuario_actual):
        """
        Obtiene el creador de contenido del usuario_actual
        :param usuario_actual: El usuario que se logeo
        :return: El CreadorDeContenido del usuario o un diccionario con el error
        """
        error = ValidacionCreadorDeContenido.validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error is not None:
            return error, 404
        creador_de_contenido = CreadorDeContenido. \
            obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        return creador_de_contenido.obtener_json()

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        """
        Se encarga de registrar un nuevo creador de contenido
        :param usuario_actual: El usuario logeado
        :return: Una lista de errores de los errores en la solictud o un diccionario con los datos del creador de
        contenido registrado
        """
        creador_de_contenido_a_registrar = CreadorDeContenido(nombre=self.argumentos['nombre'],
                                                              biografia=self.argumentos['biografia'],
                                                              es_grupo=self.argumentos['es_grupo'],
                                                              usuario_id_usuario=usuario_actual.id_usuario)
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
    def patch(self, usuario_actual):
        """
        Se encarga de responder a las peticiones de tipo put, su funcion es editar la información de un creador de
        contenido
        :param usuario_actual: El usuario logeado
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
            obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)

        creador_de_contenido.editar(creador_de_contenido_a_validar.nombre,
                                    creador_de_contenido_a_validar.biografia,
                                    creador_de_contenido_a_validar.es_grupo)

        return creador_de_contenido.obtener_json(), 202


class CreadorDeContenidoGenerosControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        """
        Se encarga de procesar una solicitud POST al agregar un Genero al CreadorDeContenido
        :param usuario_actual: El usuario logeado
        :return: El genero agregado
        """
        error_creador_no_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_no_registrado is not None:
            return error_creador_no_registrado, 400
        error_id_genero = ValidacionGenero.validar_agregar_genero(self.argumentos['id'])
        if error_id_genero is not None:
            return error_id_genero, 400
        genero = Genero.obtener_genero_por_id(self.argumentos['id'])
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        genero.agregar_creador_de_contenido(creador_de_contenido)
        return genero.obtener_json(), 201


class CreadorDeContenidoGeneroControlador(Resource):

    @token_requerido
    @solo_creador_de_contenido
    def delete(self, usuario_actual, id_genero):
        """
        Procesa una solicitud DETELE al eliminar el genero que tiene el id_genero
        :param usuario_actual: El usuario que se logeo
        :param id_genero: El id del genero a eliminar
        :return: El genero eliminado
        """
        error_creador_no_registrado = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario_actual)
        if error_creador_no_registrado is not None:
            return error_creador_no_registrado, 400
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        tiene_el_genero = creador_de_contenido.validar_tiene_genero(id_genero)
        if not tiene_el_genero:
            return None, 404
        genero = Genero.obtener_genero_por_id(id_genero)
        genero.eliminar_creador_de_contenido(creador_de_contenido)
        return genero.obtener_json(), 202


class CreadorDeContenidoPublicoControlador(Resource):

    def get(self, id_creador_de_contenido):
        """
        Se encarga de responder a una solicitud GET con la infomracion del creador que conentenga el
        id_creador_de_conenido
        :param id_creador_de_contenido: El id del creador de contenido a recuperar
        :return: Un creador de contenido
        """
        error_no_existe_creador_de_contenido = ValidacionCreadorDeContenido. \
            validar_existe_creador_de_contenido(id_creador_de_contenido)
        if error_no_existe_creador_de_contenido is not None:
            return error_no_existe_creador_de_contenido, 404
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_de_contenido)
        return creador_de_contenido.obtener_json(), 200


class CreadoresDeContenidoBuscarControlador(Resource):

    def get(self, cadena_busqueda):
        """
        Se encarga de responder una peticion GET al buscar todos los creadores de contenido que coincidan
        con la cadena de busqueda
        :param cadena_busqueda: La cadena de busqueda que se utlizara para filtrar a los creadores de contenido
        """
        cantidad = request.args.get('cantidad')
        pagina = request.args.get('pagina')
        try:
            if cantidad is not None or pagina is not None:
                cantidad = int(cantidad)
                pagina = int(pagina)
            else:
                cantidad = 10
                pagina = 1
            creadores_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_busqueda(cadena_busqueda,
                                                                                                  cantidad,
                                                                                                  pagina)
        except ValueError:
            creadores_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_busqueda(cadena_busqueda)

        creadores_de_contenido_diccionario = []
        if len(creadores_de_contenido) > 0:
            for creador_de_contenido in creadores_de_contenido:
                creadores_de_contenido_diccionario.append(creador_de_contenido.obtener_json())
        return creadores_de_contenido_diccionario
