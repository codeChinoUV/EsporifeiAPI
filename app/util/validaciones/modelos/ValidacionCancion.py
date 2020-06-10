from app.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionCancion:

    @staticmethod
    def _validar_parametros_requeridos(cancion):
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
        tamano_minino_nombre = 5
        tamano_maximo_nombre = 70
        if cancion.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(cancion.nombre, "nombre", tamano_minino_nombre,
                                                               tamano_maximo_nombre)
            return error

    @staticmethod
    def validar_registro_cancion(cancion):
        error_parametros_faltantes = ValidacionCancion._validar_parametros_requeridos(cancion)
        if error_parametros_faltantes is not None:
            return error_parametros_faltantes
        error_tamano_atributos_texto = ValidacionCancion._validar_tamano_atributos_texto(cancion)
        if error_tamano_atributos_texto is not None:
            return error_tamano_atributos_texto
