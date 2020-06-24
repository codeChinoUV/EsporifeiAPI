import threading
from concurrent.futures import thread

from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion
from app.util.validaciones.modelos.ValidacionCancionPersonal import ValidacionCancionPersonal
import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2
from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from app.administracion_de_contenido.modelo.modelos import CreadorDeContenido

from app.util.validaciones.servicios_grpc.ValidacionServiciosGrpc import ValidacionServiciosGrpc

from app.manejo_de_archivos.controlador.AdministradorDeArchivos import AdministradorDeArchivos

from Servidor.app.manejo_de_archivos.controlador.ManejadorCanciones import ManejadorCanciones


class ValidacionCancionesService:

    @staticmethod
    def _validar_existe_cancion(id_cancion):
        existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if existe_cancion is not None:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = existe_cancion['error']
            error.mensaje = existe_cancion['mensaje']
            return error

    @staticmethod
    def _validar_existe_cancion_personal(id_cancion):
        existe_cancion = ValidacionCancionPersonal.validar_existe_cancion_personal(id_cancion)
        if existe_cancion is not None:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = existe_cancion['error']
            error.mensaje = existe_cancion['mensaje']
            return error

    @staticmethod
    def _validar_es_dueno_de_cancion(token, id_cancion):
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        creador_de_contenido = CreadorDeContenido.obtener_creador_de_contenido_por_id_usuario(usuario_actual.id_usuario)
        es_dueno = ValidacionCancion.\
            validar_creador_de_contenido_es_dueno_de_cancion(id_cancion, creador_de_contenido.id_creador_de_contenido)
        if es_dueno is not None:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = es_dueno['error']
            error.mensaje = es_dueno['mensaje']
            return error

    @staticmethod
    def _validar_es_dueno_de_cancion_personal(token, id_cancion):
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        es_dueno = ValidacionCancionPersonal.validar_es_dueno_cancion_personal(usuario_actual.id_usuario, id_cancion)
        if es_dueno is not None:
            error = ManejadorDeArchivos_pb2.ErrorGeneral()
            error.error = es_dueno['error']
            error.mensaje = es_dueno['mensaje']
            return error

    @staticmethod
    def _validar_existe_cancion(id_cancion, calidad):
        existe_cancion = AdministradorDeArchivos.validar_existe_cancion_original(id_cancion)
        if not existe_cancion:
            error_no_existe_cancion = ManejadorDeArchivos_pb2.ErrorGeneral()
            error_no_existe_cancion.error = "cancion_no_existe"
            error_no_existe_cancion.mensaje = "La cancion no se encuentra registrada"
            return error_no_existe_cancion
        existe_archivo_cancion = AdministradorDeArchivos.validar_existe_archivo_cancion_original(id_cancion)
        if not existe_archivo_cancion:
            error_no_existe_cancion = ManejadorDeArchivos_pb2.ErrorGeneral()
            error_no_existe_cancion.error = "cancion_no_existe"
            error_no_existe_cancion.mensaje = "La cancion se encuentra registrada, pero no existe el archivo"
            return error_no_existe_cancion
        existe_cancion_calidad = AdministradorDeArchivos.validar_existe_cancion(id_cancion, calidad)
        if not existe_cancion_calidad:
            hilo_reconvertidor = threading.Thread(target=ManejadorCanciones.reconvertir_cancion, args=id_cancion)
            # Falta colocar el error y retornarlo

    @staticmethod
    def validar_agregar_cancion(token, id_cancion):
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token)
        if error_token_invalido is not None:
            return error_token_invalido
        error_solo_creador_de_contenido = ValidacionServiciosGrpc.validar_es_creador_de_contenido(token)
        if error_solo_creador_de_contenido is not None:
            return error_solo_creador_de_contenido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        error_no_es_dueno = ValidacionCancionesService._validar_es_dueno_de_cancion(token, id_cancion)
        if error_no_es_dueno is not None:
            return error_no_es_dueno

    @staticmethod
    def validar_agregar_cancion_personal(token, id_cancion):
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion_personal(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        error_no_es_dueno = ValidacionCancionesService._validar_es_dueno_de_cancion_personal(token, id_cancion)
        if error_no_es_dueno is not None:
            return error_no_es_dueno

    @staticmethod
    def validar_obtener_cancion(token, id_cancion):
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion

    @staticmethod
    def validar_obtener_cancion_personal(token, id_cancion):
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion_personal(id_cancion)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        # Falta validar si la cancion con la calidad indicada existe en los registros
