from flask_restful import Resource, Api

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido


class CreadoresDeContenidoBuscarControlador(Resource):
    api = Api()

    def get(self, cadena_busqueda):
        """
        Se encarga de responder una peticion GET al buscar todos los creadores de contenido que coincidan
        con la cadena de busqueda
        :param creador_de_contenido: La cadena de busqueda que se utlizara para filtrar a los creadores de contenido
        """
        creadores_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_busqueda(cadena_busqueda)
        creadores_de_contenido_diccionario = []
        if len(creadores_de_contenido) > 0:
            for creador_de_contenido in creadores_de_contenido:
                creadores_de_contenido_diccionario.append(creador_de_contenido.obtener_json())
        return creadores_de_contenido_diccionario

    @staticmethod
    def exponer_end_point(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        CreadoresDeContenidoBuscarControlador.api.add_resource(CreadoresDeContenidoBuscarControlador,
                                                               '/v1/creadores-de-contenido/buscar/<string' +
                                                               ':cadena_busqueda>')
        CreadoresDeContenidoBuscarControlador.api.init_app(app)
