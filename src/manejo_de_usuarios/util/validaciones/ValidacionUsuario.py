from src.manejo_de_usuarios.util.validaciones.ValidacioCadenas import ValidacionCadenas


class ValidacionUsuario:

    tamano_maximo_nombre_usuario = 50
    tamano_maximo_nombre = 70
    tamano_minimo_general = 5
    tamano_maximo_contrasena = 64

    @staticmethod
    def _validar_tamano_modelo_usuario(usuario, lista_de_errores):

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
    def validar_usuario(usuario):
        lista_de_errores = ValidacionUsuario._validar_campos_requeridos(usuario, {})
        if len(lista_de_errores) > 0:
            return lista_de_errores
        lista_de_errores = ValidacionUsuario._validar_tamano_modelo_usuario(usuario, lista_de_errores)
        return lista_de_errores
