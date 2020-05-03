from flask_restful import Resource, Api, reqparse

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido
from src.util.JsonBool import JsonBool
from src.util.validaciones.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadorDeContenidoControlador(Resource):
    api = Api()

    def get(self, id_creador_contenido):
        """
        Obtiene el creador de contenido que coincide con el id pasado como cadena
        :param id_creador_contenido: El id del creador de contenido que se buscara
        :return: El CreadorDeContenido que coincide con el id o 400 con el error de no existe el creador de contenido
        """
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_contenido)
        if creador_de_contenido is None:
            error = {'error': 'no_existe_creador_de_contenidp_con_el_id',
                     'mensaje': 'No existe ningun creadorDeContenido con el id indicado'}
            return error, 404
        return creador_de_contenido.obtener_json()

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador,
                                                       '/v1/creador-de-contenido/<int:id_creador_contenido>')
        CreadorDeContenidoControlador.api.init_app(app)


class CreadorDeContenidoUsuarioControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('biografia')
        self.parser.add_argument('es_grupo')
        self.argumentos = self.parser.parse_args(strict=True)

    def get(self, nombre_usuario):
        """
        Contesta una peticion get con el creador de contenido que pertenece al nombre de usuario
        :param nombre_usuario: El nombre de usuario del creador de contenido a buscar
        """
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_usuario(nombre_usuario)
        if creador_de_contenido is None:
            errores = {'errores': {'nombre_usuario': 'No se ecnuentra registrado ningun creador de contenido que '
                                                     'pertenezca a ese nombre de usuario'}}
            return errores, 400
        return creador_de_contenido.obtener_json(), 200

    def put(self, id_creador_contenido):
        """
        Se encarga de responder a las peticiones de tipo put, su funcion es editar la información de un creador de
        contenido
        :param id_creador_contenido: Es el id del creador de contenido que se desea editar
        :return: Un JSON con la informacion del objeto editada y un codigo de respuesta 200 o un JSON con una lista de
         errores y un codigo de respuesta 400
        """
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_contenido)
        if creador_de_contenido is None:
            errores = {'errores': {'id': 'No existe el id indicado'}}
            return errores, 400
        creador_de_contenido_a_validar = CreadorDeContenido(nombre=self.argumentos['nombre'],
                                                            biografia=self.argumentos['biografia'],
                                                            es_grupo=self.argumentos['es_grupo'],
                                                            usuario_nombre_usuario=creador_de_contenido.
                                                            usuario_nombre_usuario)
        errores_creador_de_contenido = ValidacionCreadorDeContenido \
            .validar_edicion_creador_de_contenido(creador_de_contenido_a_validar)
        if errores_creador_de_contenido is not None and len(errores_creador_de_contenido) > 0:
            return {'errores': errores_creador_de_contenido}, 400
        creador_de_contenido.nombre = self.argumentos['nombre']
        creador_de_contenido.biografia = self.argumentos['biografia']
        creador_de_contenido.es_grupo = JsonBool \
            .obtener_boolean_de_valor_json(self.argumentos['es_grupo'])
        CreadorDeContenido.actualizar_creador_de_contenido()
        return creador_de_contenido.obtener_json()

    def delete(self, id_creador_contenido):
        """
        Elimina de la base de datos el creador de contenido al que pertenece el id
        :id_creador_contenido: El id del creador de contenido que se eliminara
        :return: El creador de contenido que se elimino
        """
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_contenido)
        if creador_de_contenido is None:
            errores = {'errores': {'id': 'No existe el id indicado'}}
            return errores, 400
        creador_de_contenido.eliminar()
        return creador_de_contenido.obtener_json(), 200

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoUsuarioControlador.api.add_resource(CreadorDeContenidoUsuarioControlador,
                                                              '/creador-de-contenido/usuario/<string:nombre_usuario>')
        CreadorDeContenidoUsuarioControlador.api.init_app(app)
