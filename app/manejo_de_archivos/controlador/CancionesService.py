from app.manejo_de_archivos.manejador_de_archivos.ManejadorCanciones import ManejadorCanciones
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2_grpc, ManejadorDeArchivos_pb2
from app.util.validaciones.servicios_grpc.ValidacionCancionesService import ValidacionCancionesService
import logging as log


class CancionesServicer(ManejadorDeArchivos_pb2_grpc.CancionesServicer):
    logger = log.getLogger()

    def SubirCancionPersonal(self, request_iterator, context):
        """
        Sube la información de una CancionPersonal
        :param request_iterator: El iterador de los mensajes
        :param context: El contexto del mensaje
        :return: Una RespuestaSubirArchivo
        """
        cancion = bytearray()
        formato = None
        id_cancion_personal = 0
        ya_se_valido = False
        respuesta = ManejadorDeArchivos_pb2.RespuestaSolicitudSubirArchivo()
        try:
            for request in request_iterator:
                cancion += bytearray(request.data)
                formato = request.informacionCancion.formatoCancion
                id_cancion_personal = request.informacionCancion.idCancion
                if not ya_se_valido:
                    CancionesServicer.logger.info(context.peer() + " : Solicitud subir cancion personal con id " +
                                                  str(id_cancion_personal))
                    error_validacion = \
                        ValidacionCancionesService.validar_agregar_cancion_personal(request.token_autenticacion,
                                                                                    request.informacionCancion.idCancion
                                                                                    , context.peer())
                    ya_se_valido = True
                    if error_validacion is not None:
                        respuesta.error = error_validacion.error
                        return respuesta
            ManejadorCanciones.guardar_cancion_personal(cancion, id_cancion_personal, formato)
            CancionesServicer.logger.info(context.peer() + " : Cancion personal almacenada con el id " +
                                          str(id_cancion_personal))
        except Exception as ex:
            respuesta.error = ManejadorDeArchivos_pb2.Error.DESCONOCIDO
            CancionesServicer.logger.info(context.peer() + " : Error subir cancion personal " + str(ex))
            return respuesta
        return respuesta

    def SubirCancion(self, request_iterator, context):
        """
        Sube la información de una Cancion
        :param request_iterator: El iterador de los mensajes
        :param context: El contexto del mensaje
        :return: Una RespuestaSubirArchivo
        """
        cancion = bytearray()
        formato = None
        id_cancion = 0
        ya_se_valido = False
        respuesta = ManejadorDeArchivos_pb2.RespuestaSolicitudSubirArchivo()
        try:
            for request in request_iterator:
                cancion += bytearray(request.data)
                formato = request.informacionCancion.formatoCancion
                id_cancion = request.informacionCancion.idCancion
                if not ya_se_valido:
                    CancionesServicer.logger.info(context.peer() + " : Solicitud subir cancion con id " +
                                                  str(id_cancion))
                    error_validacion = \
                        ValidacionCancionesService.validar_agregar_cancion(request.token_autenticacion,
                                                                           request.informacionCancion.idCancion,
                                                                           context.peer())
                    ya_se_valido = True
                    if error_validacion is not None:
                        respuesta.error = error_validacion
                        return respuesta
            ManejadorCanciones.guardar_cancion(cancion, id_cancion, formato)
            CancionesServicer.logger.info(context.peer() + " : Cancion almacenada con el id " + str(id_cancion))
        except Exception as ex:
            respuesta.error = ManejadorDeArchivos_pb2.Error.DESCONOCIDO
            CancionesServicer.logger.info(context.peer() + " : Error subir cancion " + str(ex))
            return respuesta

        return respuesta

    def ObtenerCancion(self, request, context):
        ya_se_reviso = False
        token = request.token_autenticacion
        id_cancion = request.idCancion
        calidad = request.calidadCancionARecuperar
        respuesta = ManejadorDeArchivos_pb2.RespuestaObtenerCancion()
        CancionesServicer.logger.info(context.peer() + " : Solicitud obtener cancion con id " + str(id_cancion))
        validacion_obtener_cancion = ValidacionCancionesService.validar_obtener_cancion(token, id_cancion, calidad,
                                                                                        context.peer())
        if validacion_obtener_cancion:
            respuesta.error = validacion_obtener_cancion
            while not ya_se_reviso:
                ya_se_reviso = True
                yield respuesta
        else:
            cancion = ManejadorCanciones.obtener_archivo_audio_cancion(id_cancion, calidad)
            respuesta.formatoCancion = ManejadorDeArchivos_pb2.FormatoAudio.MP3
            for respuesta_cancion in CancionesServicer.enviar_cancion(cancion.ruta, respuesta):
                yield respuesta_cancion
            CancionesServicer.logger.info(context.peer() + " : Cancion devuelta con id " + str(id_cancion))

    def ObtenerCancionPersonal(self, request, context):
        ya_se_reviso = False
        token = request.token_autenticacion
        id_cancion_personal = request.idCancion
        calidad = request.calidadCancionARecuperar
        respuesta = ManejadorDeArchivos_pb2.RespuestaObtenerCancion()
        CancionesServicer.logger.info(context.peer() + " : Solicitud obtener cancion personal con id "
                                      + str(id_cancion_personal))
        validacion_obtener_cancion = ValidacionCancionesService.validar_obtener_cancion_personal(token,
                                                                                                 id_cancion_personal,
                                                                                                 calidad,
                                                                                                 context.peer())
        if validacion_obtener_cancion is not None:
            respuesta.error = validacion_obtener_cancion
            while not ya_se_reviso:
                ya_se_reviso = True
                yield respuesta
        else:
            cancion = ManejadorCanciones.obtener_archivo_audio_cancion_personal(id_cancion_personal, calidad)
            respuesta.formatoCancion = ManejadorDeArchivos_pb2.FormatoAudio.MP3
            for respuesta_cancion in CancionesServicer.enviar_cancion(cancion.ruta, respuesta):
                yield respuesta_cancion
            CancionesServicer.logger.info(context.peer() + " : Cancion personal devuelta con id "
                                          + str(id_cancion_personal))

    @staticmethod
    def enviar_cancion(ruta_cancion, respuesta):
        """
        Lee una cancion por bloques, lo agrega a la respuesta de una respuesta y regresa la respuesta adjuntando el
        bloque actual
        :param ruta_cancion: La ruta de la cancion a devolver
        :param respuesta: La respuesta en donde se agregara el bloque de la cancion
        :return: La respuesta con el bloque actual
        """
        tamano_chunk = 1000 * 64
        with open(ruta_cancion, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(tamano_chunk), b""):
                respuesta.data = bloque
                yield respuesta
