import grpc
import protos.ManejadorDeArchivos_pb2_grpc as ManejadorDeArchivos_pb2_grpc
import protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2



class CancionesServicer(ManejadorDeArchivos_pb2_grpc.CancionesServicer):

    def SubirCancionPersonal(self, request_iterator, context):
        cancion = bytearray()
        sha256 = ""
        formato = None
        for request in request_iterator:
            cancion += bytearray(request.data)
            sha256 = request.informacionCancion.sha256
            formato = request.informacionCancion.formatoCancion

    def SubirCancion(self, request_iterator, context):
        pass

    def ObtenerCancion(self, request, context):
        yield True

    def ObtenerCancionPersonal(self, request, context):
        yield True

