from . import api
from .controlador.v1.CreadorDeContenidoControlador import CreadorDeContenidoControlador, \
    CreadorDeContenidoPublicoControlador, CreadorDeContenidoGenerosControlador, CreadorDeContenidoGeneroControlador, \
    CreadoresDeContenidoBuscarControlador
from .controlador.v1.GenerosControlador import GenerosControlador
from .controlador.v1.AlbumesControlador import AlbumBuscarControlador
from .controlador.v1.AlbumControlador import AlbumesPublicoControlador

api.add_resource(CreadorDeContenidoControlador, '/v1/creador-de-contenido')
api.add_resource(CreadorDeContenidoGenerosControlador, '/v1/creador-de-contenido/generos')
api.add_resource(CreadorDeContenidoGeneroControlador, '/v1/creador-de-contenido/generos/<int:id_genero>')
api.add_resource(CreadorDeContenidoPublicoControlador, '/v1/creadores-de-contenido/<int:id_creador_de_contenido>')
api.add_resource(CreadoresDeContenidoBuscarControlador, '/v1/creadores-de-contenido/buscar/<string:cadena_busqueda>')
api.add_resource(GenerosControlador, '/v1/generos')
api.add_resource(CreadorDeContenidoAlbum, '/v1/creador-de-contenido/albumes/<int:id_album>')
api.add_resource(CreadorDeContenidoAlbumes, '/v1/creador-de-contenido/albumes')
api.add_resource(AlbumBuscarControlador, '/v1/albumes/buscar/<string:cadena_busqueda>')
api.add_resource(AlbumesPublicoControlador, '/v1/creadores-de-contenido/<int:id_creador_de_contenido>/albumes')
