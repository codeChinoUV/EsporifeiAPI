class ValidacionCadenas():

    @staticmethod
    def validar_tamano_cadena(cadena, tamano_minimo, tamano_maximo):
        return tamano_minimo < len(cadena) <= tamano_maximo
