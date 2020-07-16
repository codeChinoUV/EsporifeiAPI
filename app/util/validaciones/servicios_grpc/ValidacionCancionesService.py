import logging

from app.manejo_de_archivos.clientes_convertidor_archivos.ConvertidorDeArchivos import ConvertidorDeArchivos
from app.manejo_de_archivos.manejador_de_archivos.ManejadorCanciones import ManejadorCanciones
from app.util.validaciones.modelos.ValidacionCancion import ValidacionCancion
from app.util.validaciones.modelos.ValidacionCancionPersonal import ValidacionCancionPersonal
import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2
from app.manejo_de_usuarios.controlador.v1.LoginControlador import LoginControlador
from app.administracion_de_contenido.modelo.modelos import CreadorDeContenido

from app.util.validaciones.servicios_grpc.ValidacionServiciosGrpc import ValidacionServiciosGrpc

class ValidacionCancionesService:
    logger = logging.getLogger()

    @staticmethod
    def _validar_existe_cancion(id_cancion, ip):
        """
        Se encarga de validar si existe en la base datos la cancion con el id_cancion
        :param id_cancion: El id de la cancion a validar si existe
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si la cancion existe o un ManejadorDeArchivos_pb2.ErrorGeneral si no existe
        """
        existe_cancion = ValidacionCancion.validar_existe_cancion(id_cancion)
        if existe_cancion is not None:
            error = ManejadorDeArchivos_pb2.Error.CANCION_INEXISTENTE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) +
                                                    " :CANCION_INEXISTENTE")
            return error

    @staticmethod
    def _validar_existe_cancion_personal(id_cancion, ip):
        """
        Se encarga de validar si existe la cancion personal con el id indicado
        :param id_cancion: El id de la cancion personal a validar si existe
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si la cancion personal existe o un ManejadorDeArchivos_pb2.ErrorGeneral si no existe
        """
        existe_cancion = ValidacionCancionPersonal.validar_existe_cancion_personal(id_cancion)
        if existe_cancion is not None:
            error = ManejadorDeArchivos_pb2.Error.CANCION_PERSONAL_INEXISTENTE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) +
                                                    " :CANCION_PERSONAL_INEXISTENTE")
            return error

    @staticmethod
    def _validar_es_dueno_de_cancion(token, id_cancion, ip):
        """
        Se encarga de validar si la cancion con el id_cancion le pertenece al usuario logeado
        :param id_cancion: El id de la cancion a validar si el usuario es dueño
        :param token: El token del usuario logeado
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si el usuario si es dueño de la cancion o un ManejadorDeArchivos_pb2.ErrorGeneral si el usuario
         no es el dueño de la cancion
        """
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        creador_de_contenido = CreadorDeContenido.\
            obtener_creador_de_contenido_por_id_usuario_app(usuario_actual.id_usuario)
        es_dueno = ValidacionCancion.\
            validar_creador_de_contenido_es_dueno_de_cancion(id_cancion, creador_de_contenido.id_creador_de_contenido)
        if es_dueno is not None:
            error = ManejadorDeArchivos_pb2.Error.USUARIO_NO_ES_DUENO_DEL_RECURSO
            ValidacionCancionesService.logger.error(ip + " -- Operacion no permitida " + str(usuario_actual.id_usuario)
                                                    + " :USUARIO_NO_ES_DUENO_DEL_RECURSO " + str(id_cancion))
            return error

    @staticmethod
    def _validar_es_dueno_de_cancion_personal(token, id_cancion, ip):
        """
        Se encarga de validar si la cancion personal con el id_cancion le pertenece al usuario logeado
        :param id_cancion: El id de la cancion perosnal a validar si el usuario es dueño
        :param token: El token del usuario logeado
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si el usuario si es dueño de la cancion o un ManejadorDeArchivos_pb2.ErrorGeneral si el usuario
         no es el dueño de la cancion
        """
        usuario_actual = LoginControlador.token_requerido_grpc(token)
        es_dueno = ValidacionCancionPersonal.validar_es_dueno_cancion_personal(usuario_actual.id_usuario, id_cancion)
        if es_dueno is not None:
            error = ManejadorDeArchivos_pb2.Error.USUARIO_NO_ES_DUENO_DEL_RECURSO
            ValidacionCancionesService.logger.error(ip + " -- Operacion no permitida " + str(usuario_actual.id_usuario)
                                                    + " :USUARIO_NO_ES_DUENO_DEL_RECURSO " + str(id_cancion))
            return error

    @staticmethod
    def _validar_existe_cancion_en_servidor_archivos(id_cancion, calidad, ip):
        """
        Valida si existe el registro del archivo de la cancion en la base de datos con la calidad indicada
        :param id_cancion: El id de la cancion a validar si existe
        :param calidad: La calidad de la cancion a validar si existe
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si existe el registro del archivo de la cancion o un ManejadorDeArchivos_pb2.ErrorGeneral si no
        existe
        """
        existe_cancion = ManejadorCanciones.validar_existe_cancion_original(id_cancion)
        if not existe_cancion:
            error = ManejadorDeArchivos_pb2.Error.CANCION_INEXISTENTE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) +
                                                    " :CANCION_INEXISTENTE")
            return error
        existe_archivo_cancion = ManejadorCanciones.validar_existe_archivo_cancion_original(id_cancion)
        if not existe_archivo_cancion:
            error = ManejadorDeArchivos_pb2.Error.CANCION_INEXISTENTE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) +
                                                    " :CANCION_INEXISTENTE")
            return error
        existe_cancion_calidad = ManejadorCanciones.validar_existe_cancion(id_cancion, calidad)
        existe_archivo_cancion_calidad = ManejadorCanciones.validar_existe_archivo_cancion(id_cancion, calidad)
        if not existe_cancion_calidad or not existe_archivo_cancion_calidad:
            convertidor_de_archivos = ConvertidorDeArchivos()
            convertidor_de_archivos.agregar_cancion_a_cola(id_cancion)
            error_no_disponible = ManejadorDeArchivos_pb2.Error.CANCION_NO_DISPONIBLE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) + " en calidad " +
                                                    ValidacionServiciosGrpc.convertir_enum_calidad_grpc_a_str(calidad) +
                                                    " :CANCION_NO_DISPONIBLE")
            return error_no_disponible

    @staticmethod
    def _validar_existe_cancion_personal_en_servidor_archivos(id_cancion, calidad, ip):
        """
        Valida si existe el registro del archivo de la cancion en la base de datos con la calidad indicada
        :param id_cancion: El id de la cancion a validar si existe
        :param calidad: La calidad de la cancion a validar si existe
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si existe el registro del archivo de la cancion o un ManejadorDeArchivos_pb2.ErrorGeneral si no
        existe
        """
        existe_cancion_personal = ManejadorCanciones.validar_existe_cancion_personal_original(id_cancion)
        if not existe_cancion_personal:
            error = ManejadorDeArchivos_pb2.Error.CANCION_PERSONAL_INEXISTENTE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) +
                                                    " :CANCION_PERSONAL_INEXISTENTE")
            return error
        existe_archivo_cancion_personal = \
            ManejadorCanciones.validar_existe_archivo_cancion_personal_original(id_cancion)
        if not existe_archivo_cancion_personal:
            error = ManejadorDeArchivos_pb2.Error.CANCION_PERSONAL_INEXISTENTE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) +
                                                    " :CANCION_PERSONAL_INEXISTENTE")
            return error
        existe_cancion_personal_calidad = ManejadorCanciones.validar_existe_cancion_personal(id_cancion, calidad)
        existe_archivo_cancion_personal_calidad = ManejadorCanciones.validar_existe_archivo_cancion_personal(id_cancion,
                                                                                                             calidad)
        if not existe_cancion_personal_calidad or not existe_archivo_cancion_personal_calidad:
            convertidor_de_archivos = ConvertidorDeArchivos()
            convertidor_de_archivos.agregar_cancion_personal_a_cola(id_cancion)
            error_no_disponible = ManejadorDeArchivos_pb2.Error.CANCION_PERSONAL_NO_DISPONIBLE
            ValidacionCancionesService.logger.error(ip + " -- Recurso inexistente " + str(id_cancion) + " en calidad " +
                                                    ValidacionServiciosGrpc.convertir_enum_calidad_grpc_a_str(calidad) +
                                                    " :CANCION_PERSONAL_NO_DISPONIBLE")
            return error_no_disponible

    @staticmethod
    def validar_agregar_cancion(token, id_cancion, ip):
        """
        Se encarga de realizar las validaciones necesarias sobre la cancion para registrar una nueva cancion
        :param token: El token del usuario logeado
        :param id_cancion: El id de la cancion que se registrara
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si no ocurrio ningun error al momento de realizar las validaciones o
        un ManejadorDeArchivos_pb2.ErrorGeneral si ocurrio un error
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_solo_creador_de_contenido = ValidacionServiciosGrpc.validar_es_creador_de_contenido(token, ip)
        if error_solo_creador_de_contenido is not None:
            return error_solo_creador_de_contenido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion(id_cancion, ip)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        error_no_es_dueno = ValidacionCancionesService._validar_es_dueno_de_cancion(token, id_cancion, ip)
        if error_no_es_dueno is not None:
            return error_no_es_dueno

    @staticmethod
    def validar_agregar_cancion_personal(token, id_cancion, ip):
        """
        Se encarga de realizar las validaciones correspondientes al momento de agregar una cancion personal
        :param token: El token del usuario logeado
        :param id_cancion: El id de la cancion personal a agregar
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si la cancion personal cumple con lo necesario o un ManejadorDeArchivos_pb2.ErrorGeneral si no
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion_personal(id_cancion, ip)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        error_no_es_dueno = ValidacionCancionesService._validar_es_dueno_de_cancion_personal(token, id_cancion, ip)
        if error_no_es_dueno is not None:
            return error_no_es_dueno

    @staticmethod
    def validar_obtener_cancion(token, id_cancion, calidad, ip):
        """
        Realiza las validaciones necesarias para obtener una cancion
        :param token: El token del usuario logeado
        :param id_cancion: El id de la cancion a obtener
        :param calidad: La calidad de la cancion a recuperar
        :param ip: El ip del cliente del al cual se le validara su solicitud
        :return: None si la cancion con en la calidad indicada es valida o un ManejadorDeArchivos_pb2.ErrorGeneral si
         ocurrio un error en la validacion
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion(id_cancion, ip)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        error_no_existe_cancion_servidor_archivos = \
            ValidacionCancionesService._validar_existe_cancion_en_servidor_archivos(id_cancion, calidad, ip)
        if error_no_existe_cancion_servidor_archivos is not None:
            return error_no_existe_cancion_servidor_archivos

    @staticmethod
    def validar_obtener_cancion_personal(token, id_cancion, calidad, ip):
        """
        Realiza las validaciones necesarias para obtener una cancion personal
        :param token: El token del usuario logeado
        :param id_cancion: El id de la cancion personal a obtener
        :param calidad: La calidad de la cancion pesonal a recuperar
        :param ip: El ip del cliente del cual se le realizara la validación de su solicitud
        :return: None si la cancion personal con en la calidad indicada es valida o un
        ManejadorDeArchivos_pb2.ErrorGeneral si ocurrio un error en la validacion
        """
        error_token_vacio = ValidacionServiciosGrpc.validar_token_vacio(token, ip)
        if error_token_vacio is not None:
            return error_token_vacio
        error_token_invalido = ValidacionServiciosGrpc.validar_token_valido(token, ip)
        if error_token_invalido is not None:
            return error_token_invalido
        error_no_existe_cancion = ValidacionCancionesService._validar_existe_cancion_personal(id_cancion, ip)
        if error_no_existe_cancion is not None:
            return error_no_existe_cancion
        error_no_existe_cancion_servidor_archivos = \
            ValidacionCancionesService._validar_existe_cancion_personal_en_servidor_archivos(id_cancion, calidad, ip)
        if error_no_existe_cancion_servidor_archivos is not None:
            return error_no_existe_cancion_servidor_archivos
