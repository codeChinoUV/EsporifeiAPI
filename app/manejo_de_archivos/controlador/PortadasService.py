import logging

from app.manejo_de_archivos.manejador_de_archivos.MenejadorDePortadas import ManejadorDePortadas
from app.manejo_de_archivos.modelo.modelos import Portada
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2_grpc, ManejadorDeArchivos_pb2
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import RespuestaSolicitudSubirArchivo, FormatoImagen, \
    RespuestaObtenerPortada, Error
from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from app.util.validaciones.servicios_grpc.ValidacionPortadasService import ValidacionPortadasService


class PortadasServicer(ManejadorDeArchivos_pb2_grpc.PortadasServicer):

    def __init__(self):
        self.logger = logging.getLogger()

    def SubirPortadaAlbum(self, request_iterator, context):
        id_elemento = 0
        formato = None
        se_reviso = False
        respuesta = RespuestaSolicitudSubirArchivo()
        portada = bytearray()
        try:
            for request in request_iterator:
                token = request.token_autenticacion
                formato = request.informacionPortada.formatoImagen
                id_elemento = request.informacionPortada.idElementoDePortada
                portada += request.data
                if not se_reviso:
                    self.logger.info(context.peer() + ": Solicitud subir portada del album " + str(id_elemento))
                    validacion = ValidacionPortadasService.validar_subir_portada_album(token, id_elemento,
                                                                                       context.peer())
                    se_reviso = True
                    if validacion is not None:
                        respuesta.error = validacion
                        return respuesta
            ManejadorDePortadas.guardar_portada_album(portada, id_elemento, formato)
        except Exception as ex:
            self.logger.error(context.peer() + ": Error subir portada album " + str(ex))
            respuesta.error = Error.DESCONOCIDO
            return respuesta
        respuesta.error = Error.NINGUNO
        return respuesta

    def SubirPortadaCreadorDeContenido(self, request_iterator, context):
        id_elemento = 0
        formato = None
        se_reviso = False
        respuesta = RespuestaSolicitudSubirArchivo()
        portada = bytearray()
        try:
            for request in request_iterator:
                token = request.token_autenticacion
                formato = request.informacionPortada.formatoImagen
                id_elemento = request.informacionPortada.idElementoDePortada
                if not se_reviso:
                    self.logger.info(context.peer() + ": Solicitud subir portada del creador de contenido "
                                     + str(id_elemento))
                    validacion = ValidacionPortadasService.validar_subir_portada_creador_de_contenido(token,
                                                                                                      context.peer())
                    se_reviso = True
                    if validacion is not None:
                        respuesta.error = validacion
                        return respuesta
                portada += request.data
            ManejadorDePortadas.guardar_portada_creador_de_contenido(portada, id_elemento, formato)
        except Exception as ex:
            self.logger.error(context.peer() + ": Error subir portada creador de contenido " + str(ex))
            respuesta.error = Error.DESCONOCIDO
            return respuesta
        respuesta.error = Error.NINGUNO
        return respuesta

    def SubirPortadaUsuario(self, request_iterator, context):
        id_elemento = 0
        formato = None
        se_reviso = False
        respuesta = RespuestaSolicitudSubirArchivo()
        portada = bytearray()
        token = ""
        try:
            for request in request_iterator:
                token = request.token_autenticacion
                formato = request.informacionPortada.formatoImagen
                id_elemento = request.informacionPortada.idElementoDePortada
                if not se_reviso:
                    self.logger.info(context.peer() + ": Solicitud subir portada del usuario " + str(id_elemento))
                    validacion = ValidacionPortadasService.validar_subir_portada_usuario(token, context.peer())
                    se_reviso = True
                    if validacion is not None:
                        respuesta.error = validacion
                        return respuesta
                portada += request.data
            usuario_actual = LoginControlador.token_requerido_grpc(token)
            ManejadorDePortadas.guardar_portada_usuario(portada, usuario_actual.id_usuario, formato)
        except Exception as ex:
            self.logger.error(context.peer() + ": Error subir portada usuario " + str(ex))
            respuesta.error = Error.DESCONOCIDO
            return respuesta
        respuesta.error = Error.NINGUNO
        return respuesta

    def ObtenerPortadaAlbum(self, request, context):
        validacion = ValidacionPortadasService.obtener_portada_album(request.token_autenticacion,
                                                                     request.idElementoDePortada,
                                                                     request.calidadPortadaARecuperar, context.peer())
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            return respuesta

        portada = Portada.obtener_portada_album(request.idElementoDePortada, request.calidadPortadaARecuperar)
        respuesta.formatoPortada = FormatoImagen.PNG
        self.logger.info(context.peer() + ": Solicitud obtener portada del album " + str(request.idElementoDePortada))
        for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
            yield respuesta_portada
        self.logger.info(context.peer() + ": Portada enviada del album " + str(request.idElementoDePortada))

    def ObtenerPortadaCreadorDeContenido(self, request, context):
        validacion = ValidacionPortadasService.obtener_portada_creador_de_contenido(request.token_autenticacion,
                                                                                    request.idElementoDePortada,
                                                                                    request.calidadPortadaARecuperar,
                                                                                    context.peer())
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            return respuesta

        portada = Portada.obtener_portada_creador_de_contenido(request.idElementoDePortada,
                                                               request.calidadPortadaARecuperar)
        respuesta.formatoPortada = FormatoImagen.PNG
        self.logger.info(context.peer() + ": Obtener portada del creador de contenido " +
                         str(request.idElementoDePortada))
        for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
            yield respuesta_portada
        self.logger.info(context.peer() + ": Portada enviada del creador de contenido " +
                         str(request.idElementoDePortada))

    def ObtenerPortadaUsuario(self, request, context):
        validacion = ValidacionPortadasService.obtener_portada_usuario(request.token_autenticacion,
                                                                       request.idElementoDePortada,
                                                                       request.calidadPortadaARecuperar, context.peer())
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            return respuesta

        portada = Portada.obtener_portada_usuario(request.idElementoDePortada, request.calidadPortadaARecuperar)
        respuesta.formatoPortada = FormatoImagen.PNG
        self.logger.info(context.peer() + ": Obtener portada del usuario " + str(request.idElementoDePortada))
        for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
            yield respuesta_portada
        self.logger.info(context.peer() + ": Portada enviada del usaurio " + str(request.idElementoDePortada))

    @staticmethod
    def enviar_portada(ruta_portada, respuesta):
        tamano_chunk = 1000 * 64
        with open(ruta_portada, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(tamano_chunk), b""):
                respuesta.data = bloque
                yield respuesta
