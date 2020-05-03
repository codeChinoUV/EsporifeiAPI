from src.manejo_de_usuarios.modelo.enum.enums import TipoUsuario
from src.manejo_de_usuarios.modelo.modelos import Usuario
from src.util.validaciones.ValidacioCadenas import ValidacionCadenas


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
        tamano_hash_contrasena = 64
        lista_de_errores = []
        if usuario.nombre is not None:
            error = ValidacionUsuario._validar_tamano_parametro(usuario.nombre_usuario, "nombre_usuario",
                                                                tamano_minimo_general, tamano_maximo_nombre_usuario)
            if error is not None:
                lista_de_errores.append(error)
        if usuario.nombre is not None:
            error = ValidacionUsuario._validar_tamano_parametro(usuario.nombre, "nombre", tamano_minimo_general,
                                                                tamano_maximo_nombre)
            if error is not None:
                lista_de_errores.append(error)
        if usuario.contrasena is not None:
            error = ValidacionUsuario._validar_tamano_contrasena(usuario.contrasena, tamano_hash_contrasena)
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

        if len(parametros_faltantes) > 0:
            mensaje = "Los siguientes parametros faltan en tu solicitud: " + parametros_faltantes
            errores = {'error': 'parametros_faltantes', 'mensaje': mensaje}
            return errores

    @staticmethod
    def validar_usuario(usuario):
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
        return lista_de_errores

    @staticmethod
    def validar_nombre_usuario_disponible(nombre_usuario, lista_de_errores):
        """
        Valida si el nombre del usuario se encuentra disponible
        :param nombre_usuario: El nombre del usuario que se va a validar si se encuentra disponible
        :param lista_de_errores: La lista de errores del usuario
        :return: La lista de errores actualizada
        """
        if not Usuario.verificar_nombre_usuario_en_uso(nombre_usuario=nombre_usuario):
            lista_de_errores['nombre_usuario'] = "El nombre de usuario no se encuentra registrado"
        return lista_de_errores

    @staticmethod
    def validar_existe_usuario(nombre_usuario):
        """
        Valida si el nombre de usuario se encuentre registrado en la base de datos
        :param nombre_usuario: El usuario que se va a validar que exista en la base de datos
        :return: Un error que indica si el nombre_usuario se encuentra en uso o None si no se encuentra registrado
        """
        if nombre_usuario is not None and Usuario.verificar_nombre_usuario_en_uso(nombre_usuario):
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
    def validar_tipo_usuario_creador_de_contenido(nombre_usuario, lista_de_errores):
        """
        Valida que el nombre_usuario sea de tipo creador de contenido
        :param nombre_usuario: El nombre_de_usuario a validar
        :param lista_de_errores: La lista que contiene todos los errores
        :return: La lista de errores actualizada
        """
        if not Usuario.validar_usuario_creador_de_contenido(nombre_usuario):
            lista_de_errores['nombre_usuario'] = "El usuario no es un creador de contenido"
        return lista_de_errores

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
    def _validar_tamano_parametro(cadena, nombre_parametro, tamano_minimo, tamano_maximo):
        """
        Valida que el tamaño de la cadena se encuentre entre el tamano_minimo y el tamano_maximo
        :param cadena: La cadena de texto a la que se validara el tamaño
        :param tamano_minimo: El tamaño minimo que puede tener la cadena
        :param tamano_maximo: El tamaño maximo que puede tener la cadena
        :param nombre_parametro: El nombre del parametro que se utilizara para crear el diccionario con los errores
        :return: Un diccionario con los errores encontrados o None si no hay ningun error
        """
        if len(cadena) < tamano_minimo:
            error = {'error': nombre_parametro + '_demasiado_corto',
                     'mensaje': 'El <' + nombre_parametro + '> debe de tener una longitud mayor a' + tamano_minimo
                                + ' y menor a ' + tamano_maximo}
            return error
        elif len(cadena) > tamano_maximo:
            error = {'error': nombre_parametro + '_demasiado_largo',
                     'mensaje': 'El <' + nombre_parametro + '> debe de tener una longitud mayor a' + tamano_minimo
                                + ' y menor a ' + tamano_maximo}
            return error

    @staticmethod
    def _validar_tamano_contrasena(cadena, tamano_hash):
        """
        Valida que el tamaño de la cadena corresponda al tamaño_hash
        :param cadena: La cadena a validar que cumpla con el tamaño
        :param tamano_hash: El tamaño que debe de tener la cadena
        :return: Un diccionario que indica si hubo un error o None si no hubi errores
        """
        if len(cadena) != tamano_hash:
            error = {'error': 'contrasena_no_hasheada', 'mensaje': 'La <contrasena> debe de ser hasheada con el '
                                                                   'algortimo sha-256'}
            return error
