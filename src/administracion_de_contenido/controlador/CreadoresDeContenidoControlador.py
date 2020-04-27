from flask_restful import Resource, Api, reqparse

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido
from src.util.JsonBool import JsonBool
from src.util.validaciones.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido


class CreadoresDeContenidoControlador(Resource):
    """
    Se encarga de controlar el tipo de peticiones que se le le puede realizar al endpoint
    """
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('biografia')
        self.parser.add_argument('es_grupo')
        self.parser.add_argument('nombre_usuario')
        self.argumentos = self.parser.parse_args(strict=True)

    def post(self):
        """
        Se encarga de registrar un nuevo creador de contenido
        :return: Una lista de errores de los datos o los datos del nuevo creador de contenido registrado
        """
        creador_de_contenido_a_registrar = CreadorDeContenido(nombre=self.argumentos['nombre'],
                                                              biografia=self.argumentos['biografia'],
                                                              es_grupo=self.argumentos['es_grupo'],
                                                              usuario_nombre_usuario=self.argumentos['nombre_usuario'])
        errores_creador_de_contenido = \
            ValidacionCreadorDeContenido.validar_creador_de_contenido(creador_de_contenido_a_registrar)
        if len(errores_creador_de_contenido) > 0:
            errores = {'errores': errores_creador_de_contenido}
            return errores, 400
        creador_de_contenido_a_registrar.es_grupo = JsonBool \
            .obtener_boolean_de_valor_json(creador_de_contenido_a_registrar.es_grupo)
        creador_de_contenido_a_registrar.guardar()
        return creador_de_contenido_a_registrar.obtener_json()

    def get(self):
        """
        Se encarga de obtener todos los creadores de contenido registrados en la base de datos
        """
        creadores_de_contenido = CreadorDeContenido.obtener_todos_los_creadores_de_contenido()
        lista_de_creadore_de_contenido = []
        for creador_de_contenido in creadores_de_contenido:
            lista_de_creadore_de_contenido.append(creador_de_contenido.obtener_json())
        return lista_de_creadore_de_contenido

    @staticmethod
    def exponer_end_point(app):
        CreadoresDeContenidoControlador.api.add_resource(CreadoresDeContenidoControlador, '/creadores-de-contenido')
        CreadoresDeContenidoControlador.api.init_app(app)
