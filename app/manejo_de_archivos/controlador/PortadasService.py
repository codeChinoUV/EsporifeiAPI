import logging

from app.manejo_de_archivos.manejador_de_archivos.MenejadorDePortadas import ManejadorDePortadas
from app.manejo_de_archivos.modelo.modelos import Portada
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2_grpc
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import RespuestaSolicitudSubirArchivo, FormatoImagen, \
    RespuestaObtenerPortada
from app.util.validaciones.servicios_grpc.ValidacionPortadasService import ValidacionPortadasService


class PortadasServicer(ManejadorDeArchivos_pb2_grpc.PortadasServicer):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def SubirPortadaAlbum(self, request_iterator, context):
        token = ""
        id_elemento = 0
        has256 = ""
        formato = None
        se_reviso = False
        respuesta = RespuestaSolicitudSubirArchivo()
        portada = bytearray()
        for request in request_iterator:
            token = request.token_autenticacion
            formato = request.informacionPortada.formatoImagen
            id_elemento = request.informacionPortada.idElementoDePortada
            has256 = request.informacionPortada.sha256
            if not se_reviso:
                self.logger.info("Solicitud subir portada del album " + str(id_elemento))
                validacion = ValidacionPortadasService.validar_subir_portada_album(token, id_elemento)
                se_reviso = True
                if validacion is not None:
                    respuesta = validacion
                    return respuesta
            portada += respuesta.data
        ManejadorDePortadas.guardar_portada_album(portada, id_elemento, formato, has256)

    def SubirPortadaCreadorDeContenido(self, request_iterator, context):
        token = ""
        id_elemento = 0
        has256 = ""
        formato = None
        se_reviso = False
        respuesta = RespuestaSolicitudSubirArchivo()
        portada = bytearray()
        for request in request_iterator:
            token = request.token_autenticacion
            formato = request.informacionPortada.formatoImagen
            id_elemento = request.informacionPortada.idElementoDePortada
            has256 = request.informacionPortada.sha256
            if not se_reviso:
                self.logger.info("Solicitud subir portada del creador de contenido " + str(id_elemento))
                validacion = ValidacionPortadasService.validar_subir_portada_creador_de_contenido(token)
                se_reviso = True
                if validacion is not None:
                    respuesta = validacion
                    return respuesta
            portada += respuesta.data
        ManejadorDePortadas.guardar_portada_creador_de_contenido(portada, id_elemento, formato, has256)

    def SubirPortadaUsuario(self, request_iterator, context):
        token = ""
        id_elemento = 0
        has256 = ""
        formato = None
        se_reviso = False
        respuesta = RespuestaSolicitudSubirArchivo()
        portada = bytearray()
        for request in request_iterator:
            self.logger.info("Solicitud subir portada del usuario " + str(id_elemento))
            token = request.token_autenticacion
            formato = request.informacionPortada.formatoImagen
            id_elemento = request.informacionPortada.idElementoDePortada
            has256 = request.informacionPortada.sha256
            if not se_reviso:
                validacion = ValidacionPortadasService.validar_subir_portada_usuario(token)
                se_reviso = True
                if validacion is not None:
                    respuesta = validacion
                    return respuesta
            portada += respuesta.data
        ManejadorDePortadas.guardar_portada_usuario(portada, id_elemento, formato, has256)

    def ObtenerPortadaAlbum(self, request, context):
        validacion = ValidacionPortadasService.obtener_portada_album(request.token_autenticacion,
                                                                     request.idElementoDePortada,
                                                                     request.calidadPortadaARecuperar)
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            return respuesta

        portada = Portada.obtener_portada_album(request.idElementoDePortada, request.calidadPortadaARecuperar)
        respuesta.formatoPortada = FormatoImagen.PNG
        self.logger.info("Solicitud obtener portada del album " + str(request.idElementoDePortada))
        for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
            yield respuesta_portada
        self.logger.info("Portada enviada del album " + str(request.idElementoDePortada))

    def ObtenerPortadaCreadorDeContenido(self, request, context):
        validacion = ValidacionPortadasService.obtener_portada_creador_de_contenido(request.token_autenticacion,
                                                                                    request.idElementoDePortada,
                                                                                    request.calidadPortadaARecuperar)
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            return respuesta

        portada = Portada.obtener_portada_creador_de_contenido(request.idElementoDePortada,
                                                               request.calidadPortadaARecuperar)
        respuesta.formatoPortada = FormatoImagen.PNG
        self.logger.info("Obtener portada del creador de contenido " + str(request.idElementoDePortada))
        for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
            yield respuesta_portada
        self.logger.info("Portada enviada del creador de contenido " + str(request.idElementoDePortada))

    def ObtenerPortadaUsuario(self, request, context):
        validacion = ValidacionPortadasService.obtener_portada_usuario(request.token_autenticacion,
                                                                       request.idElementoDePortada,
                                                                       request.calidadPortadaARecuperar)
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            return respuesta

        portada = Portada.obtener_portada_usuario(request.idElementoDePortada, request.calidadPortadaARecuperar)
        respuesta.formatoPortada = FormatoImagen.PNG
        self.logger.info("Obtener portada del usuario " + str(request.idElementoDePortada))
        for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
            yield respuesta_portada
        self.logger.info("Portada enviada del usaurio " + str(request.idElementoDePortada))

    @staticmethod
    def enviar_portada(ruta_portada, respuesta):
        tamano_chunk = 1000 * 64
        with open(ruta_portada, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(tamano_chunk), b""):
                respuesta.data = bloque
                yield respuesta
