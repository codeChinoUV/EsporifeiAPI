from app.administracion_de_contenido.modelo.modelos import Cancion, Album
from app.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionCancion:

    @staticmethod
    def _validar_parametros_requeridos(cancion):
        """
        Valida si el objeto cancion tiene todos los parametros requeridos
        :param cancion: La cancion a validar si tienes los parametros
        :return: None si la cancion contiene los parametros requeridos o un diccionario indicando el error
        """
        parametros_faltantes = ""
        if cancion.nombre is None:
            parametros_faltantes += "<nombre> "
        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def _validar_tamano_atributos_texto(cancion):
        """
        Valida el tamaño de los atributos de la cancion sea del tamaño correcto
        :param cancion: La cancion a validar
        :return: None si los atributos de la cancion tienen el tamaño valido, o un diccionario indicando el error
        """
        tamano_minino_nombre = 2
        tamano_maximo_nombre = 70
        if cancion.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(cancion.nombre, "nombre", tamano_minino_nombre,
                                                               tamano_maximo_nombre)
            return error

    @staticmethod
    def validar_registro_cancion(cancion):
        """
        Realiza las validaciones para el registro de una cancion
        :paran cancion: La cancion a validar
        :return: None si no hubo ningun error o un diccionario indicando el error
        """
        error_parametros_faltantes = ValidacionCancion._validar_parametros_requeridos(cancion)
        if error_parametros_faltantes is not None:
            return error_parametros_faltantes
        error_tamano_atributos_texto = ValidacionCancion._validar_tamano_atributos_texto(cancion)
        if error_tamano_atributos_texto is not None:
            return error_tamano_atributos_texto

    @staticmethod
    def validar_no_existe_cancion(id_album, id_cancion):
        """
        Valida si existe una cancion con el id_cancion
        :param id_album: El id del album en donde se buscara la cancion
        :param id_cancion: El id de la cancion
        :return: None si existe una cancion o un diccionario indicando el error
        """
        error_no_existe_cancion = {'error': 'cancion_inexistente', 'mensaje': 'No existe ninguna cancion con el id '
                                                                              'indicado en el album'}
        existe_cancion = Cancion.validar_existe_cancion_en_album(id_album, id_cancion)
        if not existe_cancion:
            return error_no_existe_cancion

    @staticmethod
    def validar_creador_de_contenido_es_dueno_de_cancion(id_cancion, id_creador_de_contenido):
        """
        Valida si el creador de contenido es dueño de la cancion
        :param id_cancion: El id de la cancion a validar
        :param id_creador_de_contenido: El id del creador de contenido
        :return: None si es dueño de la cancion o un diccionario indicando el error
        """
        cancion = Cancion.obtener_cancion_por_id(id_cancion)
        es_dueno = False
        for album in cancion.albumes:
            if album.creador_de_contenido_id == id_creador_de_contenido:
                es_dueno = True
                break
        if not es_dueno:
            error = {'error': 'creador_de_contenido_no_es_propietario_de_la_cancion',
                     'mensaje': 'El creador de contenido no es propietario de la cancion'}
            return error

    @staticmethod
    def validar_tiene_genero(cancion, id_genero):
        """
        Valida si la cancion tiene el genero
        :param cancion: La cancion que se validara si tiene el genero
        :param id_genero: El id del genero a validar si esta en la cancion
        :retun: None si tiene el genero o un diccionario indicando el error
        """
        if not cancion.validar_tiene_genero(id_genero):
            error = {'error': 'cancion_no_tiene_el_genero', 'mensaje': 'La cancion no tiene ningun genero con el'
                                                                       'id indicado'}
            return error
