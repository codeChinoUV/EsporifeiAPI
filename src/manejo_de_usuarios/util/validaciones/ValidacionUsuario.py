from src.manejo_de_usuarios.util.validaciones.ValidaciomCadenas import ValidacionCadenas


class ValidacionUsuario:

    tamano_maximo_nombre_usuario = 50
    tamano_maximo_nombre = 70
    tamano_minimo_general = 5
    tamano_maximo_contrasena = 70


    @staticmethod
    def _validar_tamano_modelo_usuario(usuario):
        errores_tamano = []

        if not ValidacionCadenas.validar_tamano_cadena(usuario.nombre_usuario,
                                                       tamano_minimo=ValidacionUsuario.tamano_minimo_general,
                                                       tamano_maximo=ValidacionUsuario.tamano_maximo_nombre_usuario):
            errores_tamano.append({"nombre_usuario": "Tamaño de la cadena incorrecto"})
        if not ValidacionCadenas.validar_tamano_cadena(usuario.nombre,
                                                       tamano_minimo=ValidacionUsuario.tamano_minimo_general,
                                                       tamano_maximo=ValidacionUsuario.tamano_maximo_nombre):
            errores_tamano.append({"nombre": "Tamaño de la cadena incorrecto"})

        if not ValidacionCadenas.validar_tamano_cadena(usuario.contrasena,
                                                       tamano_minimo=ValidacionUsuario.tamano_maximo_contrasena,
                                                       tamano_maximo=ValidacionUsuario.tamano_maximo_contrasena):
            errores_tamano.append({"contrasena": "Tamaño de la cadena incorrecto"})

        return errores_tamano

    @staticmethod
    def validar_usuario(usuario):
        return ValidacionUsuario._validar_tamano_modelo_usuario(usuario)
