from flask_restful import Resource, Api

from src.administracion_de_contenido.modelo.modelos import Genero


class GenerosControlador(Resource):

    api = Api()

    def get(self):
        """
        Responde a una solicitud GET al devolver todos los generos registrados
        """
        generos = Genero.recuperar_todos_los_generos()
        lista_generos = []
        for genero in generos:
            lista_generos.append(genero.obtner_json())
        return lista_generos

    @staticmethod
    def exponer_endpoint(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        GenerosControlador.api.add_resource(GenerosControlador, '/v1/generos')
        GenerosControlador.api.init_app(app)
