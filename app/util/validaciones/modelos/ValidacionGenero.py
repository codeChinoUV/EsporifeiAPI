from app.administracion_de_contenido.modelo.modelos import Genero


class ValidacionGenero:

    @staticmethod
    def _validar_campos_requeridos(id_genero):
        """
        Valida si el id_genero no es None
        :param id_genero: El campo a validar
        :return: None si el campo no es None o un diccionario con el error y mensaje si el campo es None
        """
        if id_genero is None:
            error = {'error': 'parametros_faltantes', 'mensaje': 'Los siguientes parametros faltan en tu solicitud: '
                                                                 '<id>'}
            return error

    @staticmethod
    def validar_existe_genero(id_genero):
        """
        Valida si existe un genero con el id_genero
        :param id_genero: El id del genero a validar si existe
        :return: None si existe el genero o un diccionario con el error y mensaje si no existe el genero
        """
        try:
            id_genero = int(id_genero)
            genero = Genero.obtener_genero_por_id(id_genero)
            if genero is None:
                error = {'error': 'genero_no_existe', 'mensaje': 'No existe ningun id con el genero indicado'}
                return error
        except ValueError:
            error = {'error': 'id_no_es_entero', 'mensaje': 'El id del genero debe de ser un entero'}
            return error

    @staticmethod
    def validar_agregar_genero(id_genero):
        """
        Realiza las validaciones necesarias para agregar un genero
        :param id_genero: El id a validar
        :return: None si el id_genero no tiene ningun error o un diccionario indicando el error
        """
        error_parametros_requeridos = ValidacionGenero._validar_campos_requeridos(id_genero)
        if error_parametros_requeridos is not None:
            return error_parametros_requeridos
        error_id_no_existe = ValidacionGenero.validar_existe_genero(id_genero)
        if error_id_no_existe is not None:
            return error_id_no_existe
