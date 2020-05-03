"""
La clase validacion de cadenas se encarga de agrupar todos los metodos utiles para validar una cadena de textp
"""


class ValidacionCadenas():

    @staticmethod
    def validar_tamano_cadena(cadena, tamano_minimo, tamano_maximo, nombre_campo, error):
        """
        Valida si la cadena de texto tiene se encuentra entre la calidad minima y maxima de caracteres
        :param cadena: La cadena a valdiar
        :param tamano_minimo: El tamaño minimo que puede tener la cadena
        :param tamano_maximo: El tamaño maximo que puede tener la cadena
        :param nombre_campo: El nombre del campo que se esta validando
        :return: Un diccionario con los errores del campo o None si no se encuentra
        """
        if cadena is None:
            return False
        else:
            return tamano_minimo <= len(cadena) <= tamano_maximo

    @staticmethod
    def validar_cadena_sin_caracteres_especiales(cadena):
        """
        Valida si la cadena no contiene caracteres especiales ni espacios
        :param cadena: La cadena a validar
        :return: Verdadero si la cadena no contiene o falso si contiene
        """
        return cadena.isalnum()
