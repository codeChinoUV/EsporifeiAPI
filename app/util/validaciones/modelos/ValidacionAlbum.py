from app.util.validaciones.ValidacioCadenas import ValidacionCadenas
from app.administracion_de_contenido.modelo.modelos import Album


class ValidacionAlbum():

    @staticmethod
    def _validar_parametros_requeridos(album):
        parametros_faltantes = ""
        if album.nombre is None:
            parametros_faltantes += "<nombre>, "
        if album.anio_lanzamiento is None:
            parametros_faltantes += "<anio_lanzamiento>"

        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def _validar_tamano_atributos_texto(album):
        tamano_minino_nombre = 5
        tamano_maximo_nombre = 70
        if album.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(album.nombre, "nombre", tamano_minino_nombre,
                                                               tamano_maximo_nombre)
            return error

    @staticmethod
    def _valdidar_anio_lanzamiento(anio_lanzamiento):
        error = {'error': 'anio_lanzamineto_invalido', 'mensaje': 'El <anio_lanzamiento> debe de ser entero '
                                                                  'positivo de no mas de 4 cifras'}
        try:
            if anio_lanzamiento is not None:
                anio_lanzamiento = int(anio_lanzamiento)
                if anio_lanzamiento <= 0:
                    return error
        except ValueError:
            return error

    @staticmethod
    def validar_registro_album(album):
        lista_de_errores = []
        error_campos_requeridos = ValidacionAlbum._validar_parametros_requeridos(album)
        if error_campos_requeridos is not None:
            lista_de_errores.append(error_campos_requeridos)
        error_anio_invalido = ValidacionAlbum._valdidar_anio_lanzamiento(album.anio_lanzamiento)
        if error_anio_invalido is not None:
            lista_de_errores.append(error_anio_invalido)
        return lista_de_errores

    @staticmethod
    def validar_album_existe(id_album):
        """
        Valida si existe un álbum con el id_album
        :param id_album: El id del álbum a validar si existe
        :return: None si el álbum existe o un diccionario con el error y el mensaje del error si no existe el álbum
        """
        if not Album.verificar_album_existe(id_album):
            error = {'error': 'album_inexistente',
                     'mensaje': 'No existe ningún álbum registrado con el id_album'}
            return error