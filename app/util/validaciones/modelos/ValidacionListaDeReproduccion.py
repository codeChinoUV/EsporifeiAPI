from app.administracion_de_contenido.modelo.modelos import ListaDeReproduccion
from app.util.validaciones.ValidacioCadenas import ValidacionCadenas
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion


class ValidacionListaDeReproduccion:

    @staticmethod
    def _validar_parametros_requeridos(lista_de_reproduccion):
        """
        Valida si el objeto lista_de_reproduccion tiene todos los parametros requeridos
        :param lista_de_reproduccion: La Lista de reproduccion a validar si tienes los parametros
        :return: None si la lista de reprodccion contiene los parametros requeridos o un diccionario indicando el error
        """
        parametros_faltantes = ""
        if lista_de_reproduccion.nombre is None:
            parametros_faltantes += "<nombre> "
        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def _validar_tamano_atributos_texto(lista_de_reproduccion):
        """
        Valida si el tamano de las cadenas de los atributos de tipo texto tienen un tamano valido
        :param lista_de_reproduccion: La lista de reproduccion a validar sus atributos
        :return: Una lista de errores
        """
        tamano_minimo_general = 5
        tamano_maximo_nombre = 70
        tamano_maximo_descripcion = 300
        lista_de_errores = []
        if lista_de_reproduccion.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(lista_de_reproduccion.nombre, "nombre",
                                                               tamano_minimo_general, tamano_maximo_nombre)
            if error is not None:
                lista_de_errores.append(error)
        if lista_de_reproduccion.descripcion is not None:
            error = ValidacionCadenas.validar_tamano_parametro(lista_de_reproduccion.descripcion, "descripcion",
                                                               tamano_minimo_general, tamano_maximo_descripcion)
            if error is not None:
                lista_de_errores.append(error)
        return lista_de_errores

    @staticmethod
    def validar_registro_lista_de_reproduccion(lista_de_reproduccion):
        """
        Realiza las validaciones necesarias para el registro de una lista de reproduccion
        :param lista_de_reproduccion: La lista de reproduccion a validar
        :return: Una lista con diccionarios indicando los errores o None si no hay ningun error
        """
        lista_errores = []
        error_parametros_requeridos = ValidacionListaDeReproduccion\
            ._validar_parametros_requeridos(lista_de_reproduccion)
        if error_parametros_requeridos is not None:
            lista_errores.append(error_parametros_requeridos)
            return lista_errores
        errores_de_tamano = ValidacionListaDeReproduccion._validar_tamano_atributos_texto(lista_de_reproduccion)
        if len(errores_de_tamano) > 0:
            return errores_de_tamano
        return lista_errores

    @staticmethod
    def validar_no_existe_lista_de_reproduccion(id_lista_de_reproduccion):
        """
        Valida si no existe una lista de reproduccion
        :param id_lista_de_reproduccion: El id de la lista de reproduccion a validar si existe
        :return: None si la lista de reproduccion existe o un diccionario que indica que no existe
        """
        if not ListaDeReproduccion.validar_existe_lista_de_reproduccion(id_lista_de_reproduccion):
            error = {'error': 'lista_reproduccion_inexistente', 'mensaje': 'No existe ninguna lista de reproduccion con'
                                                                           ' el id indicado'}
            return error

    @staticmethod
    def validar_usuario_es_dueno_de_lista_de_reproduccion(id_lista_reproduccion, id_usuario):
        """
        Valida si el usuario es dueño de la lista de reproduccion
        :param id_lista_reproduccion: El id de la lista de reproduccion a validar
        :param id_usuario: El id del usuario a validar si es dueño de la lista de reproduccion
        :return: None si el usuario si es dueño o un diccionario si no es dueño
        """
        if not ListaDeReproduccion.validar_usuario_es_dueno_de_lista_de_reproduccion(id_lista_reproduccion, id_usuario):
            error = {'error': 'operacion_no_permitida', 'mensaje': 'El usuario no es dueño de la lista de reproduccion'}
            return error

    @staticmethod
    def validar_edicion_lista_de_reproduccion(lista_de_reproduccion):
        """
        Realiza las validaciones necesarias para la edicion de una lista de reproduccion
        :param lista_de_reproduccion: La lista de reproduccion a valdiar
        :return: None si la lista de reproduccion es valida o un diccionario si no
        """
        errores_validacion = []
        if lista_de_reproduccion.nombre is None and lista_de_reproduccion.descripcion is None:
            error_no_campos = {'error': 'solicitud_sin_parametros_a_modificar', 'mensaje': 'La solicitud no contiene '
                                                                                           'ningun parametro a '
                                                                                           'modificar'}
            errores_validacion.append(error_no_campos)
            return errores_validacion
        error_tamano_parametros = ValidacionListaDeReproduccion._validar_tamano_atributos_texto(lista_de_reproduccion)
        if error_tamano_parametros is not None:
            return error_tamano_parametros

    @staticmethod
    def _validar_parametros_requeridos_agregar_cancion(id_cancion):
        """
        Valida que el id_cancion no sea este vacio
        :param id_cancion: El id de la cancion a validar
        :return: Un diccionario si el id_cancion esta vacio o None si no
        """
        parametros_faltante = ""
        if id_cancion is None:
            parametros_faltante += "<id>"
        if len(parametros_faltante) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltante
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def validar_agregar_cancion(id_cancion):
        """
        Realiza las validaciones necesarias para agreagar una cancion a una lista de reproduccion
        :param id_cancion: El id de la cancion a agregar
        :return: Un diccionario si algun campo no cumple los requisitos o None si los cumple
        """
        error_parametros_faltantes = ValidacionListaDeReproduccion.\
            _validar_parametros_requeridos_agregar_cancion(id_cancion)
        if error_parametros_faltantes is not None:
            return error_parametros_faltantes
        error_cancion_no_existe = ValidacionCancion.validar_existe_cancion(id_cancion)
        if error_cancion_no_existe is not None:
            return error_cancion_no_existe
