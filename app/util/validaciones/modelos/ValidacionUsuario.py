from app.manejo_de_usuarios.modelo.enum.enums import TipoUsuario
from app.manejo_de_usuarios.modelo.modelos import Usuario
from app.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionUsuario:
    """
    Se encarga de realizar todas las validaciones referentes al modelo Usuario
    """

    @staticmethod
    def _validar_tamano_modelo_usuario(usuario):
        """
        Valida que el tamaño de todos los atributos de usuario sea valido
        :param usuario: El usuario al que se le va a validar el tamaño de los atributos
        :return: La lista con los errores de los atributos
        """
        tamano_maximo_nombre_usuario = 20
        tamano_maximo_nombre = 70
        tamano_minimo_general = 5
        lista_de_errores = []
        if usuario.nombre_usuario is not None:
            error = ValidacionCadenas.validar_tamano_parametro(usuario.nombre_usuario, "nombre_usuario",
                                                               tamano_minimo_general, tamano_maximo_nombre_usuario)
            if error is not None:
                lista_de_errores.append(error)
        if usuario.nombre is not None:
            error = ValidacionCadenas.validar_tamano_parametro(usuario.nombre, "nombre", tamano_minimo_general,
                                                               tamano_maximo_nombre)
            if error is not None:
                lista_de_errores.append(error)
        if usuario.contrasena is not None:
            error = ValidacionUsuario._validar_contrasena(usuario.contrasena)
            if error is not None:
                lista_de_errores.append(error)
        return lista_de_errores

    @staticmethod
    def _validar_campos_requeridos(usuario):
        """
        Valida que los parametros requeridos del usuario se encuentren
        :param usuario: El usuario a validar
        :return: Un diccionario con el error parametros_faltantes y su detalle o None si no hay errores
        """
        parametros_faltantes = ""
        if usuario.nombre is None:
            parametros_faltantes += "<nombre> "
        if usuario.nombre_usuario is None:
            parametros_faltantes += "<nombre_usuario> "
        if usuario.contrasena is None:
            parametros_faltantes += "<contrasena> "
        if usuario.tipo_usuario is None:
            parametros_faltantes += "<tipo_usuario>"
        if usuario.correo_electronico is None:
            parametros_faltantes += "<correo_electronico>"
        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            errores = {'error': 'parametros_faltantes', 'mensaje': mensaje}
            return errores

    @staticmethod
    def validar_registro_usuario(usuario):
        """
        Valida que un usuario sea valido para poder registrarlo
        :param usuario: El usuario a registrar
        :return: Un diccionario con los errores de cada campo
        """
        lista_de_errores = []
        errores = ValidacionUsuario._validar_campos_requeridos(usuario)
        if errores is not None:
            lista_de_errores.append(errores)
        errores = ValidacionUsuario._validar_tamano_modelo_usuario(usuario)
        if len(errores) > 0:
            for error in errores:
                lista_de_errores.append(error)
        error = ValidacionUsuario._validar_nombre_usuario_valido(usuario.nombre_usuario)
        if error is not None:
            lista_de_errores.append(error)
        error = ValidacionUsuario.validar_existe_usuario(usuario.nombre_usuario)
        if error is not None:
            lista_de_errores.append(error)
        error = ValidacionUsuario._validar_tipo_usario(usuario.tipo_usuario)
        if error is not None:
            lista_de_errores.append(error)
        error_correo_electronico = ValidacionUsuario._validar_correo_electronico(usuario.correo_electronico)
        if error_correo_electronico is not None:
            lista_de_errores.append(error_correo_electronico)
        return lista_de_errores

    @staticmethod
    def validar_existe_usuario(nombre_usuario):
        """
        Valida si el nombre de usuario se encuentre registrado en la base de datos
        :param nombre_usuario: El usuario que se va a validar que exista en la base de datos
        :return: Un error que indica si el nombre_usuario se encuentra en uso o None si no se encuentra registrado
        """
        if nombre_usuario is not None and Usuario.verificar_nombre_usuario_disponible(nombre_usuario):
            error = {'error': 'nombre_usuario_en_uso',
                     'mensaje': 'El <nombre_usuario> ya se encuentra en uso, eliga otra e intente nuevamente'}
            return error

    @staticmethod
    def _validar_tipo_usario(tipo_usuario):
        """
        Valida que el tipo de usuario del usuario se encuentre en los tipos de usuario disponibles
        :param tipo_usuario: El tipo_usuario el cual se validara que sea un TipoUsuario
        :return: Un error que indica que el tipo_usuario no es valido o None si es valido
        """
        if tipo_usuario is not None:
            try:
                TipoUsuario(int(tipo_usuario))
            except ValueError:
                error = {'error': 'tipo_usuario_valor_no_valido',
                         'mensaje': 'El <tipo_usuario> debe de ser 1:CreadorDeContenido o 2:ConsumidorDeMusica'}
                return error

    @staticmethod
    def validar_tipo_usuario_creador_de_contenido(usuario):
        """
        Valida que el usuario sea de tipo creador de contenido
        :param usuario: El usuario a validar
        :return: Un diccionario indicando el error y el mensaje del error o None si el usuario es de tipo
        creadorDeContenido
        """
        if TipoUsuario(usuario.tipo_usuario) != TipoUsuario.CreadorDeContenido:
            error = {'error': 'usuario_no_es_creador_de_contenido',
                     'mensaje': 'El usuario con el cual se atentico no es de tipo CreadorDeContenido'}
            return error

    @staticmethod
    def _validar_nombre_usuario_valido(nombre_usuario):
        """
        Valida que el nombre de usuario sea alfanumerico
        :param nombre_usuario: El nombre_usuario a validar
        :return: Un diccionario con los error o None si no hubo ningun error
        """
        if nombre_usuario is not None and \
                not ValidacionCadenas.validar_cadena_sin_caracteres_especiales(nombre_usuario):
            error = {'error': 'nombre_usuario_no_es_alfanumerico',
                     'mensaje': 'El <nombre_usuario> debe de ser alfanumerico, por lo tanto no debe de '
                                'contener caracteres especiales ni espacios, solo letras y numeros'}
            return error

    @staticmethod
    def _validar_contrasena(cadena):
        """
        Valida que el tamaño sea mayor o igual al tamano_minimo
        :param cadena: La cadena a validar que cumpla con el tamaño
        :return: Un diccionario que indica si hubo un error o None si no hubo errores
        """
        if not ValidacionCadenas.validar_contrasena(cadena):
            error = {'error': 'contrasena_no_valida', 'mensaje': 'La <contrasena> debe tener al entre 8 y 16 '
                                                                 'caracteres, al menos un dígito, al menos una '
                                                                 'minúscula y al menos una mayúscula, puede tener otros'
                                                                 ' símbolos'}
            return error

    @staticmethod
    def _validar_correo_electronico(correo_electronico):
        """
        Valida si el correo_electronico es valido y se encuentra disponible
        :param correo_electronico: EL correo_electronico a validar
        :return: None si el correo es valido o un diccionario con el error y el mensaje del error si no es valido
        """
        if correo_electronico is not None:
            error_correo_invalido = ValidacionCadenas.validar_email(correo_electronico)
            if error_correo_invalido is not None:
                return error_correo_invalido
            correo_disponible = Usuario.validar_correo_electronico_disponible(correo_electronico)
            if not correo_disponible:
                error_correo_en_uso = {'error': 'email_en_uso', 'mensaje': 'El mail ya se encuentra en uso'}
                return error_correo_en_uso

    @staticmethod
    def validar_modificar_usuario(usuario):
        """
        Valida que los atributos a modificar sean correctos
        :param usuario: El usuario al que se le validaran los atributos
        :return: Un diccionario con los errores ocurridos o None si no hay errores en los atributos
        """
        if usuario.nombre is None and usuario.contrasena is None and usuario.nombre_usuario is None and \
                usuario.correo_electronico is None:
            error = {'error': 'solicitud_sin_parametros_a_modificar',
                     'mensaje': 'La solicitud no contiene ningun parametro a modificar, los parametros que puedes '
                                'modificar son: <nombre_usuario>, <nombre>, <contrasena>, <correo_electronico>'}
            return error
        lista_de_errores = []
        errores = ValidacionUsuario._validar_tamano_modelo_usuario(usuario)
        if len(errores) > 0:
            for error in errores:
                lista_de_errores.append(error)
        error = ValidacionUsuario._validar_nombre_usuario_valido(usuario.nombre_usuario)
        if error is not None:
            lista_de_errores.append(error)
        error = ValidacionUsuario.validar_existe_usuario(usuario.nombre_usuario)
        if error is not None:
            lista_de_errores.append(error)
        error_correo_electronico = ValidacionUsuario._validar_correo_electronico(usuario.correo_electronico)
        if error_correo_electronico is not None:
            lista_de_errores.append(error_correo_electronico)
        return lista_de_errores
