from . import api
from .controlador.v1.BibliotecaPersonalControlador import BibliotecaPersonalCanciones, \
    BibliotecaPersonalCancionControlador
from .controlador.v1.CalificacionControlador import CancionCalificacionControlador
from .controlador.v1.CancionesControlador import CreadorDeContenidoAlbumCanciones, CreadorDeContenidoAlbumCancion, \
    CreadorDeContenidoAlbumCancionGeneros, CreadorDeContenidoAlbumCancionGenero, CreadoresDeContenidoAlbumesCanciones, \
    CancionesBucarControlador, CreadorDeContenidoAlbumesCancionCreadoresDeContenidoControlador, \
    CreadorDeContenidoAlbumesCancionCreadorDeContenidoControlador
from .controlador.v1.CreadorDeContenidoControlador import CreadorDeContenidoControlador, \
    CreadorDeContenidoPublicoControlador, CreadorDeContenidoGenerosControlador, CreadorDeContenidoGeneroControlador, \
    CreadoresDeContenidoBuscarControlador
from .controlador.v1.GenerosControlador import GenerosControlador, GeneroCancionControlador
from .controlador.v1.AlbumesControlador import AlbumBuscarControlador
from .controlador.v1.AlbumControlador import AlbumesPublicoControlador, CreadorDeContenidoAlbum, \
    CreadorDeContenidoAlbumes
# Creadores de contenido
from .controlador.v1.HistorialControlador import HistorialCancionControlador
from .controlador.v1.ListaDeReproduccionControlador import ListasDeReproduccionControlador, \
    ListaDeReproduccionControlador, ListaDeReproduccionCanciones, ListaDeReproduccionCancion, \
    ListaDeReproduccionBuscarControlador
from .controlador.v1.RadioControlador import RadioControlador

api.add_resource(CreadorDeContenidoControlador, '/v1/creador-de-contenido')
api.add_resource(CreadorDeContenidoPublicoControlador, '/v1/creadores-de-contenido/<int:id_creador_de_contenido>')
api.add_resource(CreadoresDeContenidoBuscarControlador, '/v1/creadores-de-contenido/buscar/<string:cadena_busqueda>')

# Creadores de contenido - generos
api.add_resource(CreadorDeContenidoGenerosControlador, '/v1/creador-de-contenido/generos')
api.add_resource(CreadorDeContenidoGeneroControlador, '/v1/creador-de-contenido/generos/<int:id_genero>')

# Generos
api.add_resource(GenerosControlador, '/v1/generos')
api.add_resource(GeneroCancionControlador, '/v1/generos/<int:id_genero>/canciones')

# Albumes
api.add_resource(CreadorDeContenidoAlbum, '/v1/creador-de-contenido/albumes/<int:id_album>')
api.add_resource(CreadorDeContenidoAlbumes, '/v1/creador-de-contenido/albumes')
api.add_resource(AlbumBuscarControlador, '/v1/albumes/buscar/<string:cadena_busqueda>')
api.add_resource(AlbumesPublicoControlador, '/v1/creadores-de-contenido/<int:id_creador_de_contenido>/albumes')

# Canciones
api.add_resource(CreadorDeContenidoAlbumCanciones, '/v1/creador-de-contenido/albumes/<int:id_album>/canciones')
api.add_resource(CreadorDeContenidoAlbumCancion, '/v1/creador-de-contenido/albumes/<int:id_album>/canciones/<int'
                                                 ':id_cancion>')
api.add_resource(CreadoresDeContenidoAlbumesCanciones, '/v1/creadores-de-contenido/<int:id_creador_de_contenido'
                                                       '>/albumes/<int:id_album>/canciones/')
api.add_resource(CancionesBucarControlador, '/v1/canciones/buscar/<string:cadena_busqueda>')

# Canciones - generos
api.add_resource(CreadorDeContenidoAlbumCancionGeneros, '/v1/creador-de-contenido/albumes/<int:id_album>/canciones/<int'
                                                        ':id_cancion>/generos')
api.add_resource(CreadorDeContenidoAlbumCancionGenero, '/v1/creador-de-contenido/albumes/<int:id_album>/canciones/<int'
                                                       ':id_cancion>/generos/<int:id_genero>')

# Canciones - creadores de contenido
api.add_resource(CreadorDeContenidoAlbumesCancionCreadoresDeContenidoControlador,
                 '/v1/creador-de-contenido/albumes/<int:id_album>/canciones/<int'
                 ':id_cancion>/creadores-de-contenido')
api.add_resource(CreadorDeContenidoAlbumesCancionCreadorDeContenidoControlador,
                 '/v1/creador-de-contenido/albumes/<int:id_album>/canciones/<int'
                 ':id_cancion>/creadores-de-contenido/<int:id_creador_contenido>')

# Calificacion
api.add_resource(CancionCalificacionControlador, '/v1/canciones/<int:id_cancion>/calificaciones')

# Lista de reproduccion
api.add_resource(ListasDeReproduccionControlador, '/v1/listas-de-reproduccion')
api.add_resource(ListaDeReproduccionControlador, '/v1/listas-de-reproduccion/<int:id_lista_de_reproduccion>')

# Lista de reproduccion canciones
api.add_resource(ListaDeReproduccionCanciones, '/v1/listas-de-reproduccion/<int:id_lista_de_reproduccion>/canciones')
api.add_resource(ListaDeReproduccionCancion, '/v1/listas-de-reproduccion/<int:id_lista_de_reproduccion>/canciones/'
                                             '<int:id_cancion>')
api.add_resource(ListaDeReproduccionBuscarControlador, '/v1/listas-de-reproduccion/buscar/<string:cadena_busqueda>')

# Historial
api.add_resource(HistorialCancionControlador, '/v1/historial-reproduccion/canciones')

# Biblioteca personal
api.add_resource(BibliotecaPersonalCanciones, '/v1/biblioteca-personal/canciones')
api.add_resource(BibliotecaPersonalCancionControlador, '/v1/biblioteca-personal/canciones/<int:id_cancion_personal>')

# Radio
api.add_resource(RadioControlador, '/v1/estacion-de-radio/<int:id_cancion>')
