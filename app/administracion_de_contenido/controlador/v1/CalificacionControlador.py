from flask_restful import Resource, reqparse

from app.administracion_de_contenido.modelo.modelos import Calificacion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from app.util.validaciones.modelos.ValidacionCalificacion import ValidacionCalificacion
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion


class CancionCalificacionControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('calificacion_estrellas')
        self.argumentos = self.parser.parse_args()

    @token_requerido
    def get(self, usuario_actual, id_cancion):
        """
        Se encarga de responder una solicitud GET al devolver la calificacion de una cancion
        :param usuario_actual: El usuario logeado
        :param id_cancion: El id de la cancion a recuperar su calificacion
        :return: Un codigo de estato HTTP
        """
        error_no_existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion, 404
        calificacion = Calificacion.obtener_calificacion(id_cancion, usuario_actual.id_usuario)
        return calificacion.obtener_json(), 200

    @token_requerido
    def post(self, usuario_actual, id_cancion):
        """
        Se encarga responder a una solicitud POST al crear una calificacion
        :param usuario_actual: El usuario logeado
        :param id_cancion: La cancion a calificar
        :return: Un diccionario y un codigo de estado
        """
        error_no_existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion, 404
        erro_ya_existe = ValidacionCalificacion.validar_existe_calificacion(usuario_actual.id_usuario, id_cancion)
        if erro_ya_existe is not None:
            return erro_ya_existe, 400
        error_validacion = ValidacionCalificacion.\
            validar_registro_calificacion(self.argumentos['calificacion_estrellas'])
        if error_validacion is not None:
            return error_validacion, 400
        calificacion = Calificacion(id_usuario=usuario_actual.id_usuario,
                                    calificacion_estrellas=self.argumentos['calificacion_estrellas'],
                                    id_cancion=id_cancion)
        calificacion.guardar()
        return calificacion.obtener_json(), 201

    @token_requerido
    def delete(self, usuario_actual, id_cancion):
        error_no_existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion, 404
        erro_no_existe = ValidacionCalificacion.validar_no_existe_calificacion(usuario_actual.id_usuario, id_cancion)
        if erro_no_existe is not None:
            return erro_no_existe, 404
        calificacion = Calificacion.obtener_calificacion(id_cancion, usuario_actual.id_usuario)
        calificacion.eliminar()
        return calificacion.obtener_json(), 202

    @token_requerido
    def put(self, usuario_actual, id_cancion):
        """
        Se encarga de procesar una solicitud de tipo PATCH al editar la calificación de la cancion
        :param usuario_actual: El usuario logeado
        :param id_cancion: El id de la cancion a editar la calificacion
        :return: Un diccionario y un codigo de estado
        """
        error_no_existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion, 404
        erro_no_existe = ValidacionCalificacion.validar_no_existe_calificacion(usuario_actual.id_usuario, id_cancion)
        if erro_no_existe is not None:
            return erro_no_existe, 404
        error_validacion = ValidacionCalificacion. \
            validar_registro_calificacion(self.argumentos['calificacion_estrellas'])
        if error_validacion is not None:
            return error_validacion, 400
        calficacion = Calificacion.obtener_calificacion(id_cancion, usuario_actual.id_usuario)
        calficacion.editar_calificacion(self.argumentos['calificacion_estrellas'])
        return calficacion.obtener_json(), 202
