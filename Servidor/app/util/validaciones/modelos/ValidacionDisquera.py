from app.util.JsonBool import JsonBool
from app.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionDisquera:

    @staticmethod
    def _validar_campos_requeridos(disquera):
        """
        Valida que los atributos requeridos se encuentren en el objeto disquera
        :param disquera: La disquera validar que tenga todos los atributos requeridos
        :return: Un diccionario con el error y su mensaje si faltan campos requeridos o None si no faltan
        """
        parametros_faltantes = ""
        if disquera.nombre is None:
            parametros_faltantes += "<nombre>"
        if disquera.direccion is None:
            parametros_faltantes += "<direccion> "
        if disquera.email is None:
            parametros_faltantes += "<email>"

        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            error = {'error': 'pametros_faltantes',
                     'mensaje': mensaje}
            return error

    @staticmethod
    def _validar_tamano_cadenas(disquera):
        """
        Valida que el tamaño de los atributos de tipo string de la disquera tengan un tamaño correcto
        :param disquera: La disquera a validar sus atributos de tipo string
        :return: Una lista con los errores encontrados en el tamaño de los atributos
        """
        tamano_minimo_general = 10
        tamano_minimo_nombre = 5
        tamano_maximo_nombre = 70
        tamano_maximo_direccion = 200
        tamano_maximo_email = 100
        lista_errores = []
        if disquera.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(disquera.nombre, "nombre", tamano_minimo_nombre,
                                                               tamano_maximo_nombre)
            if error is not None:
                lista_errores.append(error)
        if disquera.direccion is not None:
            error = ValidacionCadenas.validar_tamano_parametro(disquera.direccion, "direccion", tamano_minimo_general,
                                                               tamano_maximo_direccion)
            if error is not None:
                lista_errores.append(error)
        if disquera.email is not None:
            error = ValidacionCadenas.validar_tamano_parametro(disquera.email, "email", tamano_minimo_general,
                                                               tamano_maximo_email)
            if error is not None:
                lista_errores.append(error)
        return lista_errores

    @staticmethod
    def _validar_es_empresa_booleano(es_empresa):
        """
        Valida que es_empresa sea de tipo booleano
        :param es_empresa: El campo a validar si es booleano
        :return: None si el campo es booleano o un diccionario con el error y el mensaje si no lo es
        """
        if JsonBool.obtener_boolean_de_valor_json(es_empresa) is None:
            error = {'error': 'es_empresa_no_es_booleano',
                     'mensaje': 'El atributo <es_empresa> debe de ser booleano'}
            return error

    @staticmethod
    def validar_registro_disquera(disquera):
        """
        Realiza las validaciones necesarias sobre los atributos de la disquera para verificar que los atributos cumplan
        con las restricciones
        :param disquera: La disquera a validar
        :return: Una lista de errores
        """
        lista_de_errores = []
        error_campos_requeridos = ValidacionDisquera._validar_campos_requeridos(disquera)
        if error_campos_requeridos is not None:
            lista_de_errores.append(error_campos_requeridos)
        errores_tamano_cadenas = ValidacionDisquera._validar_tamano_cadenas(disquera)
        if len(errores_tamano_cadenas) > 0:
            for error in errores_tamano_cadenas:
                lista_de_errores.append(error)
        if disquera.email is not None:
            error_email = ValidacionCadenas.validar_email(disquera.email)
            if error_email is not None:
                lista_de_errores.append(error_email)
        if disquera.telefono is not None:
            error_telefono = ValidacionCadenas.validar_numero_telefono(disquera.telefono)
            if error_telefono is not None:
                lista_de_errores.append(error_telefono)
        if disquera.es_empresa is not None:
            error_es_empresa = ValidacionDisquera._validar_es_empresa_booleano(disquera.es_empresa)
            if error_es_empresa is not None:
                lista_de_errores.append(error_es_empresa)
        return lista_de_errores
