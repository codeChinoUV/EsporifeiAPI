from flask import request
from flask_restful import Resource, Api

from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido


class CreadorDeContenidoControlador(Resource):
    api = Api()

    def get(self, id):
        """
        Obtiene el creador de contenido que coincide con el id pasado como parametro
        :param id: El id del creador de contenido que se buscara
        :return: El CreadorDeContenido que coincide con el id o 400 con el error de no existe el creador de contenido
        """
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id(id)
        if creador_de_contenido is None:
            errores = {'errores': {'id': 'No existe el id indicado'}}
            return errores, 400
        return creador_de_contenido.obtener_json()

    @staticmethod
    def exponer_end_point(app):
        CreadorDeContenidoControlador.api.add_resource(CreadorDeContenidoControlador, '/creador-de-contenido/<int:id>')
        CreadorDeContenidoControlador.api.init_app(app)
