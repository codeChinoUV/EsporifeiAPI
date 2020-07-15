import logging

from app.manejo_de_archivos.clientes_convertidor_archivos.ConvertidorDeArchivos import ConvertidorDeArchivos
from app.manejo_de_archivos.manejador_de_archivos.MenejadorDePortadas import ManejadorDePortadas
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2
from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from app.util.validaciones.modelos.ValidacionAlbum import ValidacionAlbum
from app.util.validaciones.modelos.ValidacionCreadorDeContenido import ValidacionCreadorDeContenido
from app.util.validaciones.servicios_grpc.ValidacionServiciosGrpc import ValidacionServiciosGrpc


class ValidacionPortadasService:
    logger = logging.getLogger()

    @staticmethod
    def _validar_existe_album(id_album, ip):
        """
        Valida si existe el album con el id_album en la base de datos
        :param id_album: El id del album a validar si existe
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: None si existe el album o un ManejadorDeArchivos_pb2.Error si no rexiste
        """
        existe_album = ValidacionAlbum.validar_album_existe(id_album)
        if existe_album is not None:
            error = ManejadorDeArchivos_pb2.Error.ALBUM_INEXISTENTE
            ValidacionPortadasService.logger.error(ip + " -- Recurso inexistente " + str(id_album) +
                                                   " :ALBUM_INEXISTENTE")
            return error

    @staticmethod
    def _validar_existe_portada_usuario(id_usuario, calidad, ip):
        """
        Valida si existe la portada del usuario en la calidad original y en la calidad solicitidad
        :param id_usuario: El id del usuario al que pertenece la portada
        :param calidad: La calidad a validar si existe
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si no existe la portada del usuario o None si existe
        """
        existe_portada_original = ManejadorDePortadas.validar_existe_portada_usuario_original(id_usuario)
        if not existe_portada_original:
            error = ManejadorDeArchivos_pb2.Error.PORTADA_USUARIO_INEXISTENTE
            ValidacionPortadasService.logger.info(ip + " -- Recurso inexistente " + str(id_usuario) +
                                                  " :PORTADA_USUARIO_INEXISTENTE")
            return error
        existe_portada = ManejadorDePortadas.validar_existe_portada_usuario(id_usuario, calidad)
        if not existe_portada:
            convertidor_de_archivos = ConvertidorDeArchivos()
            convertidor_de_archivos.agregar_porada_usuario_a_cola(id_usuario)
            error = ManejadorDeArchivos_pb2.Error.PORTADA_USUARIO_NO_DISPONIBLE
            ValidacionPortadasService.logger.info(ip + " -- Recurso inexistente " + str(id_usuario) +
                                                  " calidad " +
                                                  ValidacionServiciosGrpc.convertir_enum_calidad_grpc_a_str(calidad) +
                                                  " :PORTADA_USUARIO_NO_DISPONIBLE")
            return error

    @staticmethod
    def _validar_existe_portada_creador_de_contenido(id_creador_de_contenido, calidad, ip):
        """
        Valida si existe la portada del creador de contenido en la calidad original y en la calidad solicitidad
        :param id_creador_de_contenido: El id del creador de contenido al que pertenece la portada
        :param calidad: La calidad a validar si existe
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si no existe la portada del creador de contenido o None si existe
        """
        existe_portada_original = ManejadorDePortadas. \
            validar_existe_portada_creador_de_contenido_original(id_creador_de_contenido)
        if not existe_portada_original:
            error = ManejadorDeArchivos_pb2.Error.PORTADA_CREADOR_DE_CONTENIDO_INEXISTENTE
            ValidacionPortadasService.logger.info(ip + " -- Recurso inexistente " + str(id_creador_de_contenido) +
                                                  " :PORTADA_CREADOR_DE_CONTENIDO_INEXISTENTE")
            return error
        existe_portada = ManejadorDePortadas.validar_existe_portada_creador_de_contenido(id_creador_de_contenido,
                                                                                         calidad)
        if not existe_portada:
            convertidor_de_archivos = ConvertidorDeArchivos()
            convertidor_de_archivos.agregar_portada_creador_de_contenido_a_cola(id_creador_de_contenido)
            error = ManejadorDeArchivos_pb2.Error.PORTADA_CREADOR_DE_CONTENIDO_NO_DISPONIBLE
            ValidacionPortadasService.logger.info(ip + " -- Recurso inexistente " + str(id_creador_de_contenido) +
                                                  " calidad " +
                                                  ValidacionServiciosGrpc.convertir_enum_calidad_grpc_a_str(calidad) +
                                                  " :PORTADA_CREADOR_DE_CONTENIDO_NO_DISPONIBLE")
            return error

    @staticmethod
    def _validar_existe_portada_album(id_album, calidad, ip):
        """
        Valida si existe la portada del album en la calidad original y en la calidad solicitidad
        :param id_album: El id del album al que pertenece la portada
        :param calidad: La calidad a validar si existe
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si no existe la portada del album o None si existe
        """
        existe_portada_original = ManejadorDePortadas.validar_existe_portada_album_original(id_album)
        if not existe_portada_original:
            error = ManejadorDeArchivos_pb2.Error.PORTADA_ALBUM_INEXISTENTE
            ValidacionPortadasService.logger.info(ip + " -- Recurso inexistente " + str(id_album) +
                                                  " :PORTADA_ALBUM_INEXISTENTE")
            return error
        existe_portada = ManejadorDePortadas.validar_existe_portada_album(id_album, calidad)
        if not existe_portada:
            convertidor_archivos = ConvertidorDeArchivos()
            convertidor_archivos.agregar_portada_album_a_cola(id_album)
            error = ManejadorDeArchivos_pb2.Error.PORTADA_ALBUM_NO_DISPONIBLE
            ValidacionPortadasService.logger.info(ip + " -- Recurso inexistente " + str(id_album) +
                                                  " calidad " +
                                                  ValidacionServiciosGrpc.convertir_enum_calidad_grpc_a_str(calidad) +
                                                  " :PORTADA_ALBUM_NO_DISPONIBLE")
            return error

    @staticmethod
    def _validar_tiene_creador_de_contenido(usuario, ip):
        """
        Valida si el usuario tiene un creador de contenido asociado
        :param usuario: El usuario a validar si tiene un creador de contenido asociado
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si el usuario no tiene un Creador de contenido registrado o None si
        tiene un creador de contenido registrado
        """
        error_no_tiene_creador = ValidacionCreadorDeContenido. \
            validar_usuario_no_tiene_creador_de_contenido_asociado(usuario)
        if error_no_tiene_creador is not None:
            error = ManejadorDeArchivos_pb2.Error.USUARIO_NO_TIENE_REGISTRADO_CREADOR_DE_CONTENIDO
            ValidacionPortadasService.logger.info(ip + " -- Operacion no permitida " + str(usuario.id_usuario) +
                                                  " :USUARIO_NO_TIENE_REGISTRADO_CREADOR_DE_CONTENIDO")
            return error

    @staticmethod
    def _validar_es_dueno_de_album(token, id_album, ip):
        """
        Valida si el usuario con el token es el dueño del album con el id album
        :param token: El token del usuario autenticado
        :param id_album: El id del album a validar si es dueno
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si no es dueno del album o None si lo es
        """
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        es_dueno = ValidacionAlbum.validar_creador_de_contenido_es_dueno_de_album(usuario_actual.id_usuario, id_album)
        if es_dueno is not None:
            error = ManejadorDeArchivos_pb2.Error.USUARIO_NO_ES_DUENO_DEL_RECURSO
            ValidacionPortadasService.logger.info(ip + " -- Operacion no permitida " + str(usuario_actual.id_usuario) +
                                                  " :USUARIO_NO_ES_DUENO_DEL_RECURSO " + str(id_album))
            return error

    @staticmethod
    def validar_subir_portada_usuario(token, ip):
        """
        Realiza las validaciones necesarias para subir una portada de un usuario
        :param token: El token del usuario logeado
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si ocurrio un error en la validación o None si no ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido

    @staticmethod
    def validar_subir_portada_creador_de_contenido(token, ip):
        """
        Realiza las validaciones necesarias para subir una portada de un creador de contenido
        :param token: El token del usuario logeado
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si ocurrio un error en la validación o None si no ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_solo_creador_de_contenido = ValidacionServiciosGrpc.validar_es_creador_de_contenido(token, ip)
        if error_solo_creador_de_contenido is not None:
            return error_solo_creador_de_contenido
        usuario = LoginControlador.token_requerido_grpc(token)
        error_no_tiene_creador = ValidacionPortadasService._validar_tiene_creador_de_contenido(usuario, ip)
        if error_no_tiene_creador is not None:
            return error_no_tiene_creador

    @staticmethod
    def validar_subir_portada_album(token, id_album, ip):
        """
        Realiza las validaciones necesarias para subir una portada de un album
        :param token: El token del usuario logeado
        :param id_album: El id del album de la portada a subir
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: Un ManejadorDeArchivos_pb2.Error si ocurrio un error en la validación o None si no ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_solo_creador_de_contenido = ValidacionServiciosGrpc.validar_es_creador_de_contenido(token, ip)
        if error_solo_creador_de_contenido is not None:
            return error_solo_creador_de_contenido
        error_no_existe_album = ValidacionPortadasService._validar_existe_album(id_album, ip)
        if error_no_existe_album is not None:
            return error_no_existe_album
        error_no_es_dueno = ValidacionPortadasService._validar_es_dueno_de_album(token, id_album, ip)
        if error_no_es_dueno is not None:
            return error_no_es_dueno

    @staticmethod
    def obtener_portada_usuario(token, id_usuario, calidad, ip):
        """
        Realiza las validaciones necesarias para obtener una portada de un usuario
        :param token: El token del usuario autenticado
        :param id_usuario: El id del usuario a recuperar la portada
        :param calidad: La calidad de la portada a recuperar
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: None si no ocurrio un error en la validacion o un ManejadorDeArchivos_pb2.Error si ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_portada = ValidacionPortadasService._validar_existe_portada_usuario(id_usuario, calidad, ip)
        if error_no_existe_portada is not None:
            return error_no_existe_portada

    @staticmethod
    def obtener_portada_creador_de_contenido(token, id_creador_de_contenido, calidad, ip):
        """
        Realiza las validaciones necesarias para obtener una portada de un creador de contenido
        :param token: El token del usuario autenticado
        :param id_creador_de_contenido: El id del creador de contenido a recuperar su portada
        :param calidad: La calidad de la portada a recuperar
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: None si no ocurrio un error en la validacion o un ManejadorDeArchivos_pb2.Error si ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_portada = ValidacionPortadasService. \
            _validar_existe_portada_creador_de_contenido(id_creador_de_contenido, calidad, ip)
        if error_no_existe_portada is not None:
            return error_no_existe_portada

    @staticmethod
    def obtener_portada_album(token, id_album, calidad, ip):
        """
        Realiza las validaciones necesarias para obtener una portada de un album
        :param token: El token del usuario autenticado
        :param id_album: El id del album a recuperar la portada
        :param calidad: La calidad de la portada a recuperar
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: None si no ocurrio un error en la validacion o un ManejadorDeArchivos_pb2.Error si ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_album = ValidacionPortadasService._validar_existe_album(id_album, ip)
        if error_no_existe_album is not None:
            return error_no_existe_album
        error_no_existe_portada = ValidacionPortadasService._validar_existe_portada_album(id_album, calidad, ip)
        if error_no_existe_portada is not None:
            return error_no_existe_portada
