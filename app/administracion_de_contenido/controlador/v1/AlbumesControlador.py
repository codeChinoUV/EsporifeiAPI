from flask_restful import Resource

from app.administracion_de_contenido.modelo.modelos import Album

class AlbumBuscarControlador(Resource):
    def get(self, cadena_busqueda):
        """
        Se encarga de responder una peticion GET al buscar todos los álbumes que coincidan
        con la cadena de busqueda
        :param cadena_busqueda: La cadena de busqueda que se utlizara para filtrar los álbumes
        """
        albumes = Album.obtener_album_por_busqueda(cadena_busqueda)
        albumes_diccionario = []
        if len(albumes) > 0:
            for album in albumes:
                albumes_diccionario.append(album.obtener_json())
        return albumes_diccionario