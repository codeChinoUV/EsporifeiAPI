from flask_restful import Resource, reqparse

from app.administracion_de_contenido.modelo.modelos import ListaDeReproduccion
from app.manejo_de_usuarios.controlador.v1.LoginControlador import token_requerido
from app.util.validaciones.modelos.ValidacionListaDeReproduccion import ValidacionListaDeReproduccion


class ListasDeReproduccionControlador(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('descripcion')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    def get(self, usuario_actual):
        """
        Se encarga de responder a una solicitud GET al recuperar todas las listas de reproduccion de un usuario
        :param usuario_actual: El usuario del cual se recuperaran las listas de reproduccion
        :return: Un diccionario y un codigo de estado
        """
        listas_de_reproduccion = ListaDeReproduccion.\
            obtener_listas_de_reproduccion_de_usuario(usuario_actual.id_usuario)
        diccionario_de_listas = []
        for lista_de_reproduccion in listas_de_reproduccion:
            diccionario_de_listas.append(lista_de_reproduccion.obtener_json())
        return diccionario_de_listas, 200

    @token_requerido
    def post(self, usuario_actual):
        """
        Se encarga de procesar una solicitud POST al registrar una lista de reproduccion al usuario actual
        :param usuario_actual: El usuario al cual se le registrara la lista de reproduccion
        :return: Un diccionario y un codigo de estado
        """
        lista_de_reproduccion = ListaDeReproduccion(nombre=self.argumentos['nombre'],
                                                    descripcion=self.argumentos['descripcion'])
        errores_validacion = ValidacionListaDeReproduccion.validar_registro_lista_de_reproduccion(lista_de_reproduccion)
        if len(errores_validacion) > 0:
            return errores_validacion, 400
        lista_de_reproduccion.usuario_id = usuario_actual.id_usuario
        lista_de_reproduccion.guardar()
        return lista_de_reproduccion.obtener_json(), 201
