from flask_restful import Resource

from app.administracion_de_contenido.modelo.modelos import Genero


class GenerosControlador(Resource):

    def get(self):
        """
        Responde a una solicitud GET al devolver todos los generos registrados
        """
        generos = Genero.recuperar_todos_los_generos()
        lista_generos = []
        for genero in generos:
            lista_generos.append(genero.obtener_json())
        return lista_generos
