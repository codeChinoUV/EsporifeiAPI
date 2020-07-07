import logging

from app.manejo_de_archivos.controlador.ManejadorDeArchivos import ManejadorDeArchivos
from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2
from app.manejo_de_usuarios.modelo.enum.enums import TipoUsuario


class ValidacionServiciosGrpc:
    logger = logging.getLogger(__name__)

    @staticmethod
    def validar_token_valido(token):
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        if usuario_actual is None:
            error = ManejadorDeArchivos_pb2.Error()
            error.errorAutenticacion = ManejadorDeArchivos_pb2.ErrorAutenticacion.TOKEN_INVALIDO
            ValidacionServiciosGrpc.logger.info("Error autenticacion: TOKEN_INVALIDO")
            return error

    @staticmethod
    def validar_token_vacio(token):
        if token is None or token == "":
            error = ManejadorDeArchivos_pb2.Error()
            error.errorAutenticacion = ManejadorDeArchivos_pb2.ErrorAutenticacion.TOKEN_FALTANTE
            ValidacionServiciosGrpc.logger.info("Error autenticacion: TOKEN_FALTANTE")
            return error

    @staticmethod
    def validar_es_creador_de_contenido(token):
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        if TipoUsuario(usuario_actual.tipo_usuario) != TipoUsuario.CreadorDeContenido:
            error = ManejadorDeArchivos_pb2.Error()
            error.errorOperacionNoPermitida.errorOperacionNoPermitida = ManejadorDeArchivos_pb2. \
                ErrorOperacionNoPermitida.OPERACION_NO_PERMITIDA
            ValidacionServiciosGrpc.logger.info("Operacion no permitida " + str(usuario_actual.id_usuario)
                                                + ": OPERACION_NO_PERMITIDA")
            return error

    @staticmethod
    def validar_sha256_coinciden(sha256_cancion_original, cancion):
        sha256_cancion_subida = ManejadorDeArchivos.obtener_sha256_de_byte_array(cancion)
        if sha256_cancion_original != sha256_cancion_subida:
            error = ManejadorDeArchivos_pb2.Error()
            error.errorSeguridad = ManejadorDeArchivos_pb2.ErrorSeguridad.HASH_NO_COINCIDE
            return error
