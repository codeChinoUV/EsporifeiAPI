from src.manejo_de_usuarios.modelo.Usuario import Usuario
from src.manejo_de_usuarios.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionUsuario:
    """
    Se encarga de realizar todas las validaciones referentes al modelo Usuario
    """
    tamano_maximo_nombre_usuario = 20
    tamano_maximo_nombre = 70
    tamano_minimo_general = 5
    tamano_maximo_contrasena = 64

    @staticmethod
    def _validar_tamano_modelo_usuario(usuario, lista_de_errores):
        """
        Valida que el tamaño de todos los atributos de usuario sea valido
        :param usuario: El usuario al que se le va a valdiar los atributos
        :param lista_de_errores: La lista de los errores del usuario
        :return: La lista de errores actualizada
        """
        if not ValidacionCadenas.validar_tamano_cadena(usuario.nombre_usuario,
                                                       tamano_minimo=ValidacionUsuario.tamano_minimo_general,
                                                       tamano_maximo=ValidacionUsuario.tamano_maximo_nombre_usuario):
            lista_de_errores['nombre_usuario'] = "Tamaño de la cadena incorrecto"
        if not ValidacionCadenas.validar_tamano_cadena(usuario.nombre,
                                                       tamano_minimo=ValidacionUsuario.tamano_minimo_general,
                                                       tamano_maximo=ValidacionUsuario.tamano_maximo_nombre):
            lista_de_errores['nombre'] = "Tamaño de la cadena incorrecto"

        if not ValidacionCadenas.validar_tamano_cadena(usuario.contrasena,
                                                       tamano_minimo=ValidacionUsuario.tamano_maximo_contrasena,
                                                       tamano_maximo=ValidacionUsuario.tamano_maximo_contrasena):
            lista_de_errores['contrasena'] = "Tamaño de la cadena incorrecto" + str(len(usuario.contrasena))

        return lista_de_errores

    @staticmethod
    def _validar_campos_requeridos(usuario, lista_de_errores):
        """
        Valida que los campos requeridos del usuario
        :param usuario: El usuario a validar
        :param lista_de_errores: La lista de errores del usuario
        :return: La lista de errores actualizada
        """
        if usuario.nombre is None:
            lista_de_errores['nombre'] = "El campo es requerido"
        if usuario.nombre_usuario is None:
            lista_de_errores['nombre_usuario'] = "El campo es requerido"
        if usuario.contrasena is None:
            lista_de_errores['contrasena'] = "El campo es requerido"
        if usuario.tipo_usuario is None:
            lista_de_errores['tipo_usuario'] = "El campo es requerido"

        return lista_de_errores

    @staticmethod
    def validar_usuario_consumidor_de_musica(usuario):
        """
        Valida que un usuario de tipo consumidor de musica sea valido para poder registrarlo
        :param usuario: El usuario a registrar
        :return: Un diccionario con los errores de cada campo
        """
        lista_de_errores = ValidacionUsuario._validar_campos_requeridos(usuario, {})
        if len(lista_de_errores) > 0:
            return lista_de_errores
        lista_de_errores = ValidacionUsuario._validar_tamano_modelo_usuario(usuario, lista_de_errores)
        lista_de_errores = ValidacionUsuario._validar_usuario_tipo_consumidor(usuario, lista_de_errores)
        lista_de_errores = ValidacionUsuario._validar_nombre_usuario_disponible(usuario, lista_de_errores)
        return lista_de_errores

    @staticmethod
    def _validar_usuario_tipo_consumidor(usuario, lista_de_errores):
        """
        Valida que el tipo de usuario sea consumidor de musica
        :param usuario: El usuario que se va a validar
        :param lista_de_errores: La lista de errores del usuario
        :return: La lista de errores actualizada
        """
        if usuario.tipo_usuario == 1:
            lista_de_errores['tipo_usuario'] = "En el end point solo se permite el registro de usuarios consumidores " \
                                               "de musica, para el registro de creadores de contenido dirigirse a " \
                                               "/usuarios/creador_de_contenido"
        return lista_de_errores

    @staticmethod
    def _validar_nombre_usuario_disponible(usuario, lista_de_errores):
        """
        Valida si el nombre del usuario se encuentra disponibles
        :param usuario: El usuario al que se le va a validar el nombre de usuario
        :param lista_de_errores: La lista de errores del usuario
        :return: La lista de errores actualizada
        """
        if not Usuario.verificar_nombre_usuario_disponible(usuario.nombre_usuario):
            lista_de_errores['nombre_usuario'] = "El nombre de usuario ya se encuentra en uso"
        return lista_de_errores
