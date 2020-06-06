"""
La clase validacion de cadenas se encarga de agrupar todos los metodos utiles para validar una cadena de textp
"""
import re

import phonenumbers


class ValidacionCadenas:

    @staticmethod
    def validar_tamano_parametro(cadena, nombre_parametro, tamano_minimo, tamano_maximo):
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
                     'mensaje': 'El <' + nombre_parametro + '> debe de tener una longitud mayor a ' + str(tamano_minimo)
                                + ' y menor a ' + str(tamano_maximo)}
            return error
        elif len(cadena) > tamano_maximo:
            error = {'error': nombre_parametro + '_demasiado_largo',
                     'mensaje': 'El <' + nombre_parametro + '> debe de tener una longitud mayor a' + str(tamano_minimo)
                                + ' y menor a ' + str(tamano_maximo)}
            return error

    @staticmethod
    def validar_cadena_sin_caracteres_especiales(cadena):
        """
        Valida si la cadena no contiene caracteres especiales ni espacios
        :param cadena: La cadena a validar
        :return: Verdadero si la cadena no contiene o falso si contiene
        """
        return cadena.isalnum()

    @staticmethod
    def validar_contrasena(cadena):
        """
        Valida que la cadena coincida con la expresión regular
        :param cadena: La cadena  a validar si cumple con la expresión regular
        :return: Verdadero si la cadena cumple con la expresión regular o Falso si no
        """
        expresion_regular_contrasena = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')
        if expresion_regular_contrasena.match(cadena) is None:
            return False
        else:
            return True

    @staticmethod
    def validar_numero_telefono(numero_telefono):
        """
        Valida si el numero_telefono es un numero valido
        :param numero_telefono: El numero de telefono a validar
        :return: None si el numero de telefono es valido o Un diccionario indicando el codigo del error y su mensaje
        """
        error = {'error': 'telefono_no_valido', 'mensaje': 'El <telefono> no es un numero de telefono valido'}
        try:
            numero_telefonico = phonenumbers.parse(numero_telefono, None)
            if not phonenumbers.is_possible_number(numero_telefonico):
                return error
        except phonenumbers.phonenumberutil.NumberParseException:
            return error

    @staticmethod
    def validar_email(email):
        """
        Valida que una dicreccion de email sea valida utilizando la expresion regular que proporciona la w3.org
        :param email: El email a validar
        :return: None si la direccion de email es correcta o un diccionario con el error si no
        """
        expresion_regular_email = re.compile(r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$')
        if expresion_regular_email.match(email) is None:
            error = {'error': 'email_formato_incorrecto', 'mensaje': 'El <email> no tiene un formato correcto'}
            return error
