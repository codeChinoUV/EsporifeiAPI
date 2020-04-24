from src.administracion_de_contenido.modelo.modelos import CreadorDeContenido
from src.util.JsonBool import JsonBool
from src.util.validaciones.ValidacioCadenas import ValidacionCadenas
from src.util.validaciones.ValidacionUsuario import ValidacionUsuario


class ValidacionCreadorDeContenido:
    """
    Se encarga de realizar las validaciones necesarias para el modelo CreadorDeContenido
    """
    tamano_minimo_general = 5
    tamano_maximo_nombre_usuario = 20
    tamano_maximo_nombre = 70
    tamano_maximo_biografia = 500

    @staticmethod
    def _validar_campos_requeridos(creador_de_contenido, lista_de_errores):
        """
        Valida que el creador_de_contenido tenga los campos requeridos
        :param creador_de_contenido: El creador de contenido a validar
        :param lista_de_errores: La lista de errores del creador de contenido
        :return: La lista de errores actualizada
        """
        if creador_de_contenido.nombre is None:
            lista_de_errores['nombre'] = "El campo es requerido"
        if creador_de_contenido.es_grupo is None:
            lista_de_errores['es_grupo'] = "El campo es requerido"
        if creador_de_contenido.usuario_nombre_usuario is None:
            lista_de_errores['nombre_usuario'] = "El campo es requerido"
        return lista_de_errores

    @staticmethod
    def _validar_booleano_valido(creador_de_contenido, lista_de_errores):
        """
        Valida que los campos que son de tipo booleano del creador de contenido sean validos
        :param creador_de_contenido: El creador de contenido al que se le validara los campos booleanos
        :param lista_de_errores: La lista de errores de del creador de contenid
        :return: La lista de errores actualizada
        """
        if JsonBool.obtener_boolean_de_valor_json(creador_de_contenido.es_grupo) is None:
            lista_de_errores['es_grupo'] += "Debe de ser un valor booleano"
        return lista_de_errores

    @staticmethod
    def _validar_tamano_modelo_creador_de_contenido(creador_de_contenido, lista_de_errores):
        """
        Valida que el tamaño de las cadenas de los atributos del creador_de_contenido sea valida
        :param creador_de_contenido: El creador de contenido a validar
        :param lista_de_errores: La lista de errores del creador de contenido
        :return: La lista de errores actualizada
        """
        if not ValidacionCadenas.validar_tamano_cadena(creador_de_contenido.nombre,
                                                       ValidacionCreadorDeContenido.tamano_minimo_general,
                                                       ValidacionCreadorDeContenido.tamano_maximo_nombre):
            lista_de_errores['nombre'] = "El tamaño de la cadena incorrecto"
        if creador_de_contenido.biografia is not None and not ValidacionCadenas. \
                validar_tamano_cadena(creador_de_contenido.biografia,
                                      ValidacionCreadorDeContenido.tamano_minimo_general,
                                      ValidacionCreadorDeContenido.tamano_maximo_biografia):
            lista_de_errores['biografia'] = "El tamaño de la cadena es incorrecto"
        if not ValidacionCadenas.validar_tamano_cadena(creador_de_contenido.usuario_nombre_usuario,
                                                       ValidacionCreadorDeContenido.tamano_minimo_general,
                                                       ValidacionCreadorDeContenido.tamano_maximo_nombre_usuario):
            lista_de_errores['nombre_usuario'] = "El tamaño de la cadena es incorreto"
        return lista_de_errores

    @staticmethod
    def validar_creador_de_contenido(creador_de_contenido):
        """
        Valida que el creador de contenido sea valido para poder registrarlo
        :param creador_de_contenido: El creador de contenido a validar
        :return: Un diccionario con los errores del modelo
        """
        lista_de_errores = ValidacionCreadorDeContenido._validar_campos_requeridos(creador_de_contenido, {})
        if len(lista_de_errores) > 0:
            return lista_de_errores
        lista_de_errores = ValidacionCreadorDeContenido._validar_tamano_modelo_creador_de_contenido(
            creador_de_contenido, lista_de_errores)
        if len(lista_de_errores) > 0:
            return lista_de_errores
        lista_de_errores = ValidacionCreadorDeContenido._validar_booleano_valido(creador_de_contenido, lista_de_errores)
        if len(lista_de_errores) > 0:
            return lista_de_errores
        lista_de_errores = ValidacionUsuario.validar_nombre_usuario_disponible(
            creador_de_contenido.usuario_nombre_usuario,
            lista_de_errores)
        if len(lista_de_errores) > 0:
            return lista_de_errores
        lista_de_errores = ValidacionCreadorDeContenido \
            ._validar_nombre_usuario_tiene_perfil(creador_de_contenido.usuario_nombre_usuario, lista_de_errores)
        return lista_de_errores

    @staticmethod
    def _validar_nombre_usuario_tiene_perfil(nombre_usuario, lista_errores):
        """
        Valida que el nombre de usuario no tenga un perfil asociado, si lo tiene agrega el error a la lista de errores
        :param nombre_usuario: El nombre de usuario a validar
        :param lista_errores: La lista de errores a la que se agregara el error
        :return: La lista de errores actualizada
        """
        if CreadorDeContenido.verificar_usuario_ya_tiene_perfil(nombre_usuario):
            lista_errores['nombre_usuario'] = "El usuario ya tiene un perfil registrado"
        return lista_errores
