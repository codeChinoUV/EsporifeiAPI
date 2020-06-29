import grpc
import protos.ManejadorDeArchivos_pb2_grpc as ManejadorDeArchivos_pb2_grpc
import protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2

from app.util.validaciones.servicios_grpc.ValidacionCancionesService import ValidacionCancionesService

from app.manejo_de_archivos.controlador.ManejadorCanciones import ManejadorCanciones


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
        ManejadorCanciones.guardar_cancion_personal(cancion, id_cancion_personal, formato, sha256)

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
        ManejadorCanciones.guardar_cancion(cancion, id_cancion, formato, sha256)

    def ObtenerCancion(self, request, context):
        pass

    def ObtenerCancionPersonal(self, request, context):
        pass
