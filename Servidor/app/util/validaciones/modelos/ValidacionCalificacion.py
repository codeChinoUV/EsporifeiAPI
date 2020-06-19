from app.administracion_de_contenido.modelo.modelos import Calificacion


class ValidacionCalificacion:

    @staticmethod
    def validar_existe_calificacion(id_usuario, id_cancion):
        """
        Valida si existe una Calificacion con el id_usuario y el id_cancion
        :param id_usuario: El id del usuario que realizo la calificacion
        :param id_cancion: El id de la cancion calificada
        :return: Un diccionario indicando que existe una calificacion registrada o None si no
        """
        calificacion = Calificacion.obtener_calificacion(id_cancion, id_usuario)
        if calificacion is not None:
            error = {'error': 'calificacion_registrada', 'mensaje': 'Ya existe una calificacion registrada'}
            return error

    @staticmethod
    def validar_no_existe_calificacion(id_usuario, id_cancion):
        """
        Valida si no existe una Calificacion con el id_usuario y el id_cancion
        :param id_usuario: El id del usuario que realizo la calificacion
        :param id_cancion: El id de la cancion calificada
        :return: Un diccionario indicando que no existe una calificacion registrada o None si existe
        """
        calificacion = Calificacion.obtener_calificacion(id_cancion, id_usuario)
        if calificacion is None:
            error = {'error': 'calificacion_inexistente', 'mensaje': 'No existe una calificacion registrada para la'
                                                                     ' cancion con el id_cancion'}
            return error

    @staticmethod
    def _validar_parametros_requeridos(calificacion):
        """
        Valida si la calificacion no es None
        :param calificacion: La calificacion a validar
        :return: Nose si se encuentran los parametros requerdios o un diccionario indicando el error
        """
        parametros_faltantes = ""
        if calificacion is None:
            parametros_faltantes += "calificacion_estrellas"
        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def _validar_calificacion_valida(calificacion):
        """
        Valida que la calificacion sea un entero y se encuentre entre 1 y 5
        :param calificacion: La calificacion a validar
        """
        if calificacion is not None:
            error = {'error': 'calificacion_estrellas_invalida', 'mensaje': 'La <calificacion_estrellas> debe de ser '
                                                                            'un entero entre 1 y 5'}
            try:
                calificacion = int(calificacion)
                if calificacion <= 0 or calificacion >= 6:
                    return error
            except ValueError:
                return error

    @staticmethod
    def validar_registro_calificacion(calificacion_estrellas):
        """
        Se encarga de realizar las validaciones correspondientes para el registro de la calificacion
        :param calificacion_estrellas: La calificacion a validar
        :return: Un diccionario indicando el error o None si no hay errores
        """
        error_parametros_faltantes = ValidacionCalificacion._validar_parametros_requeridos(calificacion_estrellas)
        if error_parametros_faltantes is not None:
            return error_parametros_faltantes
        error_calificacion_invalida = ValidacionCalificacion._validar_calificacion_valida(calificacion_estrellas)
        if error_calificacion_invalida is not None:
            return error_calificacion_invalida