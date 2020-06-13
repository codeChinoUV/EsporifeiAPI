from app.util.validaciones.ValidacioCadenas import ValidacionCadenas


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
        error_parametros_requeridos = ValidacionListaDeReproduccion\
            ._validar_parametros_requeridos(lista_de_reproduccion)
        if error_parametros_requeridos is not None:
            return error_parametros_requeridos
        errores_de_tamano = ValidacionListaDeReproduccion._validar_tamano_atributos_texto(lista_de_reproduccion)
        if len(errores_de_tamano) > 0:
            return errores_de_tamano
