from . import api
from .controlador.v1.CreadorDeContenidoControlador import CreadorDeContenidoControlador, \
    CreadorDeContenidoPublicoControlador
from .controlador.v1.CreadoresDeContenidoControlador import CreadoresDeContenidoBuscarControlador
from .controlador.v1.GenerosControlador import GenerosControlador

api.add_resource(CreadorDeContenidoControlador, '/v1/creador-de-contenido')
api.add_resource(CreadorDeContenidoPublicoControlador, '/v1/creadores-de-contenido/<int:id_creador_de_contenido>')
api.add_resource(CreadoresDeContenidoBuscarControlador, '/v1/creadores-de-contenido/buscar/<string:cadena_busqueda>')
api.add_resource(GenerosControlador, '/v1/generos')
