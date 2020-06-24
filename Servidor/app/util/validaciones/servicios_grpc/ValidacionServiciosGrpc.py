from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2
from app.manejo_de_usuarios.modelo.enum.enums import TipoUsuario
from app.manejo_de_archivos.controlador.AdministradorDeArchivos import AdministradorDeArchivos


class ValidacionServiciosGrpc:

    @staticmethod
    def validar_token_valido(token):
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        if usuario_actual is None:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = "token_invalido"
            error.mensaje = "El token no es valido, ya sea por que se modifico o el tiempo de vida expiro"
            return error

    @staticmethod
    def validar_token_vacio(token):
        if token is None or token == "":
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = "token_faltante"
            error.mensaje = "El token falta en la solicitud de grpc"
            return error

    @staticmethod
    def validar_es_creador_de_contenido(token):
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        if TipoUsuario(usuario_actual.tipo_usuario) != TipoUsuario.CreadorDeContenido:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = "operacion_no_permitida"
            error.mensaje = "El usuario con el que se encuentra autenticado no tiene permisos para realizar dicha " \
                            "operación"
            return error

    @staticmethod
    def validar_sha256_coinciden(sha256_cancion_original, cancion):
        sha256_cancion_subida = AdministradorDeArchivos.obtener_sha256_de_byte_array(cancion)
        if sha256_cancion_original != sha256_cancion_subida:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = "sha256_no_coincide"
            error.mensaje = "La cancion recibida no coincide con el hash de la cancion enviada"
            return error
