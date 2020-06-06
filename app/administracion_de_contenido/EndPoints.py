from . import api
from .controlador.v1.AlbumControlador import CreadorDeContenidoAlbumes, CreadorDeContenidoAlbum
from .controlador.v1.CreadorDeContenidoControlador import CreadorDeContenidoControlador, ArtistasControlador, \
    ArtistaControlador, ArtistasPublicoControlador
from .controlador.v1.CreadoresDeContenidoControlador import CreadoresDeContenidoBuscarControlador
from .controlador.v1.GenerosControlador import GenerosControlador

api.add_resource(CreadorDeContenidoControlador, '/v1/creador-de-contenido')
api.add_resource(ArtistasControlador, '/v1/creador-de-contenido/artistas')
api.add_resource(ArtistaControlador, '/v1/creador-de-contenido/artista/<int:id_artista>')
api.add_resource(ArtistasPublicoControlador, '/v1/creador-de-contenido/<int:id_creador_de_contenido>/artistas')
api.add_resource(GenerosControlador, '/v1/generos')
api.add_resource(CreadoresDeContenidoBuscarControlador, '/v1/creadores-de-contenido/buscar/<string:cadena_busqueda>')
api.add_resource(CreadorDeContenidoAlbumes, '/v1/creador-de-contenido/albumes')
api.add_resource(CreadorDeContenidoAlbum, '/v1/creador-de-contenido/albumes/<int:id_album>')
