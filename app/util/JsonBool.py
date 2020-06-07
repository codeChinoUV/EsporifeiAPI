class JsonBool:
    """
    Se encarga de convertir un valor json a booleano
    """

    @staticmethod
    def obtener_boolean_de_valor_json(valor_json):
        """
        Se encarga de convertir un valor json a booleano
        :param valor_json: El valor json a convertir
        :return: Un booleano del valor json o None si el valor json no son validos
        """
        if valor_json == 'true' or valor_json == 'True' or valor_json == True:
            return True
        elif valor_json == 'false' or valor_json == 'False' or valor_json == False:
            return False
        else:
            return None
