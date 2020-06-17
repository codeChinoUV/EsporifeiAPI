from app.administracion_de_contenido.modelo.modelos import CancionPersonal
from app.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionCancionPersonal:

    @staticmethod
    def _validar_campos_requeridos(cancion_personal):
        """
        Valida que el objeto CancionPersonal tiene los parametros requeridos
        :param cancion_personal: La cancionPersonal a validar
        :return: None si tiene los parametros requeridos o un diccionario con el error
        """
        parametros_faltantes = ""
        if cancion_personal.nombre is None:
            parametros_faltantes += "<nombre>, "
        if cancion_personal.artistas is None:
            parametros_faltantes += "<artistas> "

        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            errores = {'error': 'parametros_faltantes', 'mensaje': mensaje}
            return errores

    @staticmethod
    def _validar_tamano_parametros_texto(cancion_personal):
        """
        Valida si el tamaño de los atributos del objeto cancion tienen la longitud permitida
        :param cancion_personal: La cancion a validar sus atributus
        :return: Una lista de errores
        """
        tamano_minimo_general = 3
        tamano_maximo_general = 70
        lista_de_errores = []
        if cancion_personal.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(cancion_personal.nombre, "nombre",
                                                               tamano_minimo_general, tamano_maximo_general)
            if error is not None:
                lista_de_errores.append(error)
        if cancion_personal.artistas is not None:
            error = ValidacionCadenas.validar_tamano_parametro(cancion_personal.artistas, "artistas",
                                                               tamano_minimo_general, tamano_maximo_general)
            if error is not None:
                lista_de_errores.append(error)
        if cancion_personal.album is not None:
            error = ValidacionCadenas.validar_tamano_parametro(cancion_personal.album, "album",
                                                               tamano_minimo_general, tamano_maximo_general)
            if error is not None:
                lista_de_errores.append(error)
        return lista_de_errores

    @staticmethod
    def _validar_cantidad_canciones_de_usuario(id_usuario):
        """
        Valida la cantidad de canciones que tiene el usuario
        :param id_usuario: El id del usuario a validar la cantidad de canciones
        :return: None si aun no supera el maximo de canciones
        """
        maximo_canciones_permitido = 250
        cantidad_canciones = CancionPersonal.obtener_cantidad_de_canciones(id_usuario)
        if cantidad_canciones > maximo_canciones_permitido:
            error_maximo_permitido = {'error': 'maximo_canciones_superada', 'mensaje': 'Se ha superado el maximo de '
                                                                                       'canciones en la biblioteca '
                                                                                       'personal'}
            return error_maximo_permitido

    @staticmethod
    def validar_registro_cancion_personal(cancion_personal):
        """
        Valida que el objeto cumpla con todas las restricciones para el registro del campo
        :param cancion_personal: La cancion personal a validar
        :return: Un diccionario con el error o None si no hay errores
        """
        error_parametros = ValidacionCancionPersonal._validar_campos_requeridos(cancion_personal)
        if error_parametros is not None:
            return error_parametros
        error_tamano_parametros_texto = ValidacionCancionPersonal._validar_tamano_parametros_texto(cancion_personal)
        if len(error_tamano_parametros_texto) > 0:
            return error_tamano_parametros_texto
        error_cantidad_de_canciones = ValidacionCancionPersonal.\
            _validar_cantidad_canciones_de_usuario(cancion_personal.id_usuario)
        if error_cantidad_de_canciones is not None:
            return error_cantidad_de_canciones
