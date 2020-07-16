import logging

from app.manejo_de_archivos.manejador_de_archivos.ManejadorDeArchivos import ManejadorDeArchivos
from app.manejo_de_archivos.manejador_de_archivos.MenejadorDePortadas import ManejadorDePortadas
from app.manejo_de_archivos.modelo.modelos import Portada
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2_grpc
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import RespuestaSolicitudSubirArchivo, FormatoImagen, \
    RespuestaObtenerPortada, Error
from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from app.util.validaciones.servicios_grpc.ValidacionPortadasService import ValidacionPortadasService


class PortadasServicer(ManejadorDeArchivos_pb2_grpc.PortadasServicer):

    def __init__(self):
        self.logger = logging.getLogger()

    def SubirPortadaAlbum(self, request_iterator, context):
        """
        Se ecnarga de subir la portada de un album
        :param request_iterator: El iterador de la solicitud
        :param context: El contexto de la solicitud
        :return: Una RespuestaSubirArchivo con el tipo de error ocurrido
        """
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
        """
        Se ecnarga de subir la portada de un creador de contenido
        :param request_iterator: El iterador de la solicitud
        :param context: El contexto de la solicitud
        :return: Una RespuestaSubirArchivo con el tipo de error ocurrido
        """
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
        """
        Se ecnarga de subir la portada de un usuario
        :param request_iterator: El iterador de la solicitud
        :param context: El contexto de la solicitud
        :return: Una RespuestaSubirArchivo con el tipo de error ocurrido
        """
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
        """
        Se encarga de recuperar la portada de un Album
        :param request: La solicitud
        :param context: El contexto de la solicitud
        :return: Un stream de RespuestaObtenerPortada
        """
        ya_se_reviso = False
        validacion = ValidacionPortadasService.obtener_portada_album(request.token_autenticacion,
                                                                     request.idElementoDePortada,
                                                                     request.calidadPortadaARecuperar, context.peer())
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            while not ya_se_reviso:
                ya_se_reviso = True
                yield respuesta
        else:
            calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(request.calidadPortadaARecuperar)
            portada = Portada.obtener_portada_album(request.idElementoDePortada, calidad)
            respuesta.formatoPortada = FormatoImagen.PNG
            self.logger.info(context.peer() + ": Solicitud obtener portada del album " +
                             str(request.idElementoDePortada))
            for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
                yield respuesta_portada
            self.logger.info(context.peer() + ": Portada enviada del album " + str(request.idElementoDePortada))

    def ObtenerPortadaCreadorDeContenido(self, request, context):
        """
        Se encarga de recuperar la portada de un CreadorDeContenido
        :param request: La solicitud
        :param context: El contexto de la solicitud
        :return: Un stream de RespuestaObtenerPortada
        """
        ya_se_reviso = False
        validacion = ValidacionPortadasService.obtener_portada_creador_de_contenido(request.token_autenticacion,
                                                                                    request.idElementoDePortada,
                                                                                    request.calidadPortadaARecuperar,
                                                                                    context.peer())
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            while not ya_se_reviso:
                ya_se_reviso = True
                yield respuesta
        else:
            calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(request.calidadPortadaARecuperar)
            portada = Portada.obtener_portada_creador_de_contenido(request.idElementoDePortada, calidad)
            respuesta.formatoPortada = FormatoImagen.PNG
            self.logger.info(context.peer() + ": Obtener portada del creador de contenido " +
                             str(request.idElementoDePortada))
            for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
                yield respuesta_portada
            self.logger.info(context.peer() + ": Portada enviada del creador de contenido " +
                             str(request.idElementoDePortada))

    def ObtenerPortadaUsuario(self, request, context):
        """
        Se encarga de recuperar la portada de un Usuario
        :param request: La solicitud
        :param context: El contexto de la solicitud
        :return: Un stream de RespuestaObtenerPortada
        """
        ya_se_reviso = False
        validacion = ValidacionPortadasService.obtener_portada_usuario(request.token_autenticacion,
                                                                       request.idElementoDePortada,
                                                                       request.calidadPortadaARecuperar, context.peer())
        respuesta = RespuestaObtenerPortada()
        if validacion is not None:
            respuesta.error = validacion
            while not ya_se_reviso:
                ya_se_reviso = True
                yield respuesta
        else:
            calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(request.calidadPortadaARecuperar)
            portada = Portada.obtener_portada_usuario(request.idElementoDePortada, calidad)
            respuesta.formatoPortada = FormatoImagen.PNG
            self.logger.info(context.peer() + ": Obtener portada del usuario " + str(request.idElementoDePortada))
            for respuesta_portada in PortadasServicer.enviar_portada(portada.ruta, respuesta):
                yield respuesta_portada
            self.logger.info(context.peer() + ": Portada enviada del usaurio " + str(request.idElementoDePortada))

    @staticmethod
    def enviar_portada(ruta_portada, respuesta):
        """
        Se encarga de agregar los bytes de la portada a la respuesta
        :param ruta_portada: La ruta de la portada a regresar
        :param respuesta: La respuesta en donde se agregaran los bytes de la portada
        :return: La respuesta con los bytes de la portada
        """
        tamano_chunk = 1000 * 64
        with open(ruta_portada, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(tamano_chunk), b""):
                respuesta.data = bloque
                yield respuesta
