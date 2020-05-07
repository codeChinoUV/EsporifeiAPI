from src.administracion_de_contenido.modelo.modelos import Artista
from src.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionArtista:
    """
    Se encarga de realizar las validaciones necesarias para el modelo Artista
    """

    @staticmethod
    def _validar_campos_requeridos(artista):
        """
        Valida que los atributos requeridos se encuentren en el objeto artista
        :param artista: El artista a validar que tenga todos los atributos requeridos
        :return: Un diccionario con el error y su mensaje si faltan campos requeridos o None si no faltan
        """
        parametros_faltantes = ""
        if artista.nombre is None:
            parametros_faltantes += "<nombre>"

        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def _validar_tamano_atributos(artista):
        """
        Se encarga de validar el tamano de los atributos del objeto artista
        :param artista: El artitsta al que se le validara el tamaño de sus atributos
        :return: Un diccionario con el error y su mensaje o None si todos los tamaños son validos
        """
        tamano_minimo_nombre = 5
        tamano_maximo_nombre = 70
        if artista.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(artista.nombre, "nombre", tamano_minimo_nombre,
                                                               tamano_maximo_nombre)
            return error

    @staticmethod
    def validar_registro_artista(artista):
        """
        Realiza las validaciones necesarias para asegurar que el artista se pueda registrar de manera correcta
        :param artista: El artista que se validara
        :return: Una lista con los errores encontrados
        """
        lista_de_errores = []
        error_campos_requeridos = ValidacionArtista._validar_campos_requeridos(artista)
        if error_campos_requeridos is not None:
            lista_de_errores.append(error_campos_requeridos)
        error_tamano_campos = ValidacionArtista._validar_tamano_atributos(artista)
        if error_tamano_campos is not None:
            lista_de_errores.append(error_tamano_campos)
        return lista_de_errores

    @staticmethod
    def validar_artista_existe(id_artista):
        """
        Valida si existe un artista con el id_artista
        :param id_artista: El id del artista a validar si existe
        :return: None si el artista existe o un diccionario con el error y el mensaje del error si no exitse el artista
        """
        if not Artista.verificar_artista_existe(id_artista):
            error = {'error': 'artista_inexistente',
                     'mensaje': 'No existe ningun artista registrado con el id_artista'}
            return error

    @staticmethod
    def validar_usuario_es_dueno_de_artista(id_creador_de_contenido, id_artista):
        """
        Valida que el creador de contenido sea el dueño del artista al que intenta acceder
        :param id_creador_de_contenido: El id del creador de contenido a validar que es el dueño del artista
        :param id_artista: El id del artista a validar que pertenece al creador de contenido
        """
        if not Artista.verificar_creador_de_contenido_es_dueno_de_artista(id_creador_de_contenido, id_artista):
            error = {'error': 'el_usuario_no_es_el_dueno_de_la_informacion',
                     'mensaje': 'El usuario atenticado no es dueño de la información a la que intenta tener acceso'}
            return error
