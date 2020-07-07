from app.manejo_de_archivos.manejador_de_archivos.ManejadorCanciones import ManejadorCanciones
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2_grpc, ManejadorDeArchivos_pb2
from app.util.validaciones.servicios_grpc.ValidacionCancionesService import ValidacionCancionesService

from app.util.validaciones.servicios_grpc.ValidacionServiciosGrpc import ValidacionServiciosGrpc


class CancionesServicer(ManejadorDeArchivos_pb2_grpc.CancionesServicer):

    def SubirCancionPersonal(self, request_iterator, context):
        cancion = bytearray()
        sha256 = ""
        formato = None
        id_cancion_personal = 0
        ya_se_valido = False
        respuesta = ManejadorDeArchivos_pb2.RespuestaSolicitudSubirArchivo()
        for request in request_iterator:
            cancion += bytearray(request.data)
            sha256 = request.informacionCancion.sha256
            formato = request.informacionCancion.formatoCancion
            id_cancion_personal = request.informacionCancion.idCancion
            if not ya_se_valido:
                error_validacion = \
                    ValidacionCancionesService.validar_agregar_cancion_personal(request.token_autenticacion,
                                                                                request.informacionCancion.idCancion)
                ya_se_valido = True
                if error_validacion is not None:
                    respuesta.error = error_validacion.error
                    return respuesta
        hash256_valido = ValidacionServiciosGrpc.validar_sha256_coinciden(sha256, cancion)
        if hash256_valido is not None:
            respuesta.error = hash256_valido.error
            return respuesta
        ManejadorCanciones.guardar_cancion_personal(cancion, id_cancion_personal, formato, sha256)
        return respuesta

    def SubirCancion(self, request_iterator, context):
        cancion = bytearray()
        sha256 = ""
        formato = None
        id_cancion = 0
        ya_se_valido = False
        respuesta = ManejadorDeArchivos_pb2.RespuestaSolicitudSubirArchivo()
        for request in request_iterator:
            cancion += bytearray(request.data)
            sha256 = request.informacionCancion.sha256
            formato = request.informacionCancion.formatoCancion
            id_cancion = request.informacionCancion.idCancion
            if not ya_se_valido:
                error_validacion = \
                    ValidacionCancionesService.validar_agregar_cancion(request.token_autenticacion,
                                                                       request.informacionCancion.idCancion)
                ya_se_valido = True
                if error_validacion is not None:
                    respuesta.error = error_validacion.error
                    return respuesta
        hash256_valido = ValidacionServiciosGrpc.validar_sha256_coinciden(sha256, cancion)
        if hash256_valido is not None:
            respuesta.error = hash256_valido.error
            return respuesta
        ManejadorCanciones.guardar_cancion(cancion, id_cancion, formato, sha256)
        return respuesta

    def ObtenerCancion(self, request, context):
        token = request.token_autenticacion
        id_cancion = request.idCancion
        calidad = request.calidad
        respuesta = ManejadorDeArchivos_pb2.RespuestaObtenerCancion()
        validacion_obtener_cancion = ValidacionCancionesService.validar_obtener_cancion(token, id_cancion, calidad)
        if validacion_obtener_cancion is not None:
            respuesta.error = validacion_obtener_cancion
            return validacion_obtener_cancion
        cancion = ManejadorCanciones.obtener_archivo_audio_cancion(id_cancion, calidad)
        respuesta.formato = ManejadorDeArchivos_pb2.FormatoAudio.MP3
        for respuesta_cancion in CancionesServicer.enviar_cancion(cancion.ruta, respuesta):
            yield respuesta_cancion

    def ObtenerCancionPersonal(self, request, context):
        token = request.token_autenticacion
        id_cancion_personal = request.idCancion
        calidad = request.calidad
        respuesta = ManejadorDeArchivos_pb2.RespuestaObtenerCancion()
        validacion_obtener_cancion = ValidacionCancionesService.validar_obtener_cancion_personal(token,
                                                                                                 id_cancion_personal,
                                                                                                 calidad)
        if validacion_obtener_cancion is not None:
            respuesta.error = validacion_obtener_cancion
            return validacion_obtener_cancion
        cancion = ManejadorCanciones.obtener_archivo_audio_cancion_personal(id_cancion_personal, calidad)
        respuesta.formato = ManejadorDeArchivos_pb2.FormatoAudio.MP3
        for respuesta_cancion in CancionesServicer.enviar_cancion(cancion.ruta, respuesta):
            yield respuesta_cancion

    @staticmethod
    def enviar_cancion(ruta_cancion, respuesta):
        tamano_chunk = 1000 * 64
        with open(ruta_cancion, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(tamano_chunk), b""):
                respuesta.data = bloque
                yield respuesta
