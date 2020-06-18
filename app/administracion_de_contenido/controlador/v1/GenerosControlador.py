from flask import request
from flask_restful import Resource

from app.administracion_de_contenido.modelo.modelos import Genero
from app.util.validaciones.modelos.ValidacionGenero import ValidacionGenero


class GenerosControlador(Resource):

    def get(self):
        """
        Responde a una solicitud GET al devolver todos los generos registrados
        :return: Una lista de diccionarios y un codigo de estado
        """
        generos = Genero.recuperar_todos_los_generos()
        lista_generos = []
        for genero in generos:
            lista_generos.append(genero.obtener_json())
        return lista_generos


class GeneroCancionControlador(Resource):

    def get(self, id_genero):
        """
        Se encarga de procesar una solicitud de tipo GET al devolver las canciones del genero, ordenda por cantidad de
        reproducciones
        :param id_genero: El id del genero a recuperar
        :return: Una lista de diccionario y un codigo estado
        """
        error_no_existe_genero = ValidacionGenero.validar_existe_genero(id_genero)
        if error_no_existe_genero is not None:
            return error_no_existe_genero, 404
        cantidad = request.args.get('cantidad')
        pagina = request.args.get('pagina')
        try:
            if cantidad is not None and pagina is not None:
                cantidad = int(cantidad)
                pagina = int(pagina)
            else:
                cantidad = 10
                pagina = 1
            canciones = Genero.obtener_canciones_por_genero(id_genero, cantidad, pagina)
        except ValueError:
            canciones = Genero.obtener_canciones_por_genero(id_genero)
        canciones_dicionario = []
        for cancion in canciones:
            canciones_dicionario.append(cancion.obtener_json_con_album())
        return canciones_dicionario, 200


class GeneroCreadorDeContenido(Resource):

    def get(self, id_genero):
        """
        Se encarga de procesar una solicitud de tipo GET al devolver los creadores de contenido del genero, ordenda
        por nombre
        :param id_genero: El id del genero a recuperar
        :return: Una lista de diccionario y un codigo estado
        """
        error_no_existe_genero = ValidacionGenero.validar_existe_genero(id_genero)
        if error_no_existe_genero is not None:
            return error_no_existe_genero, 404
        cantidad = request.args.get('cantidad')
        pagina = request.args.get('pagina')
        try:
            if cantidad is not None and pagina is not None:
                cantidad = int(cantidad)
                pagina = int(pagina)
            else:
                cantidad = 10
                pagina = 1
            creadores_de_contenido = Genero.obtener_cradores_de_contenido_por_genero(id_genero, cantidad, pagina)
        except ValueError:
            creadores_de_contenido = Genero.obtener_cradores_de_contenido_por_genero(id_genero)
        creadores_de_contenido_lista = []
        for creador_de_contenido in creadores_de_contenido:
            creadores_de_contenido_lista.append(creador_de_contenido.obtener_json())
        return creadores_de_contenido_lista, 200
