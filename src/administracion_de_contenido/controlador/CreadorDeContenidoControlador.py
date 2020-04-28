from flask_restful import Resource, Api, reqparse

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido
from src.util.JsonBool import JsonBool
from src.util.validaciones.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadorDeContenidoControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('biografia')
        self.parser.add_argument('es_grupo')
        self.argumentos = self.parser.parse_args(strict=True)

    def get(self, id_creador_contenido):
        """
        Obtiene el creador de contenido que coincide con el id pasado como parametro
        :param id_creador_contenido: El id del creador de contenido que se buscara
        :return: El CreadorDeContenido que coincide con el id o 400 con el error de no existe el creador de contenido
        """
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id_creador_contenido)
        if creador_de_contenido is None:
            errores = {'errores': {'id_creador_contenido': 'No existe el id indicado'}}
            return errores, 401
        return creador_de_contenido.obtener_json()

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

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador,
                                                       '/creador-de-contenido/<int:id_creador_contenido>')
        CreadorDeContenidoControlador.api.init_app(app)
