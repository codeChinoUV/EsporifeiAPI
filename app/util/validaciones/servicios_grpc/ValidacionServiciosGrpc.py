import logging

from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2
from app.manejo_de_usuarios.modelo.enum.enums import TipoUsuario


class ValidacionServiciosGrpc:
    logger = logging.getLogger()

    @staticmethod
    def validar_token_valido(token, ip):
        """
        Valida que el token es un token valido
        :param token: El token a validar
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si el token es valido o un ManejadorDeArchivos_pb2.Error.TOKEN_INVALIDO
        """
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        if usuario_actual is None:
            error = ManejadorDeArchivos_pb2.Error.TOKEN_INVALIDO
            ValidacionServiciosGrpc.logger.info(ip + " -- Error autenticacion: TOKEN_INVALIDO")
            return error

    @staticmethod
    def validar_token_vacio(token, ip):
        """
        Valida si el token enviado por el cliente no esta vacio
        :param token: El token a validar
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si el token no esta vacio o un ManejadorDeArchivos_pb2.Error.TOKEN_FALTANTE
        """
        if token is None or token == "":
            error = ManejadorDeArchivos_pb2.Error.TOKEN_FALTANTE
            ValidacionServiciosGrpc.logger.info(ip + " -- Error autenticacion: TOKEN_FALTANTE")
            return error

    @staticmethod
    def validar_es_creador_de_contenido(token, ip):
        """
        Valida si el token del cliente pertence a un creador de contenido
        :param token: El token a validar
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si el token pertenece a un usuario CreadorDeContenido o un
        ManejadorDeArchivos_pb2.Error.OPERACION_NO_PERMITIDA
        """
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        if TipoUsuario(usuario_actual.tipo_usuario) != TipoUsuario.CreadorDeContenido:
            error = ManejadorDeArchivos_pb2.Error.OPERACION_NO_PERMITIDA
            ValidacionServiciosGrpc.logger.info(ip + " -- Operacion no permitida " + str(usuario_actual.id_usuario)
                                                + ": OPERACION_NO_PERMITIDA")
            return error

    @staticmethod
    def convertir_enum_calidad_grpc_a_str(calidad):
        """
        Convierte un enum Calidad a su equivalente a texto
        :param calidad: El enum Calidad a convertir
        :return: La representacion del enum a string
        """
        calidad_str = ""
        if calidad == ManejadorDeArchivos_pb2.Calidad.ALTA:
            calidad_str = "alta"
        elif calidad == ManejadorDeArchivos_pb2.Calidad.MEDIA:
            calidad_str = "media"
        elif calidad == ManejadorDeArchivos_pb2.Calidad.BAJA:
            calidad_str = "baja"
        return calidad_str
