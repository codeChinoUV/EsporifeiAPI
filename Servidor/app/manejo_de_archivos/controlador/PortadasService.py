import grpc
import protos.ManejadorDeArchivos_pb2_grpc as ManejadorDeArchivos_pb2_grpc
import protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2

class PortadasServicer(ManejadorDeArchivos_pb2_grpc.PortadasServicer):

    def SubirPortadaAlbum(self, request_iterator, context):
        pass

    def SubirPortadaCreadorDeContenido(self, request_iterator, context):
        pass

    def SubirPortadaUsuario(self, request_iterator, context):
        pass

    def SubirPortadaListaDeReproduccion(self, request_iterator, context):
        pass

    def ObtenerPortadaAlbum(self, request, context):
        yield True

    def ObtenerPortadaCreadorDeContenido(self, request, context):
        yield True

    def ObtenerPortadaUsuario(self, request, context):
        yield True

    def ObtenerPortadaListaDeReproduccion(self, request, context):
        yield True