import logging
import threading
import time

from app.manejo_de_archivos.manejador_de_archivos.ManejadorDeArchivos import ManejadorDeArchivos
from app.manejo_de_archivos.modelo.modelos import Portada
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import Calidad

from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import FormatoImagen
import cv2
from app.manejo_de_archivos.clientes_convertidor_archivos.ClienteConvertidorImagenes import \
    ConvertidorDeImagenesCliente
from app.manejo_de_archivos.clientes_convertidor_archivos.enums.TipoPortada import TipoPortada


class ManejadorDePortadas:
    logger = logging.getLogger(__name__)

    @staticmethod
    def validar_existe_portada_usuario_original(id_usuario):
        """
        Valida si existe la portada en calidad original de un usuario
        :param id_usuario: El id del usuario a validar si tiene una portada registrada
        :return: Verdadero si existe la portada original del usario o falso si no
        """
        portada = Portada.obtener_portada_usuario(id_usuario, Calidad.ORIGINAL)
        return portada is not None

    @staticmethod
    def validar_existe_portada_usuario(id_usuario, calidad):
        """
        Valida si existe la portada de un usuario
        :param id_usuario: El id del usuario a validar si tiene una portada registrada
        :param calidad: La calidad de la portada a validar si existe
        :return: Verdadero si existe la portada del usario o falso si no
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        portada = Portada.obtener_portada_usuario(id_usuario, calidad)
        return portada is not None

    @staticmethod
    def validar_existe_portada_creador_de_contenido_original(id_creador_de_contenido):
        """
        Valida si existe la portada en calidad original de un creador de contenido
        :param id_creador_de_contenido: El id del creador de contenido a validar si tiene una portada registrada
        :return: Verdadero si existe la portada original del creador de contenido o falso si no
        """
        portada = Portada.obtener_portada_creador_de_contenido(id_creador_de_contenido, Calidad.ORIGINAL)
        return portada is not None

    @staticmethod
    def validar_existe_portada_creador_de_contenido(id_creador_de_contenido, calidad):
        """
        Valida si existe la portada de un creador de contenido
        :param id_creador_de_contenido: El id del creador de contenido a validar si tiene una portada registrada
        :param calidad: La calidad de la portada a validar si existe
        :return: Verdadero si existe la portada del creador de contendio o falso si no
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        portada = Portada.obtener_portada_creador_de_contenido(id_creador_de_contenido, calidad)
        return portada is not None

    @staticmethod
    def validar_existe_portada_album_original(id_album):
        """"
        Valida si existe la portada en calidad original de un album
        :param id_album: El id del album a validar si tiene una portada registrada
        :return: Verdadero si existe la portada original del album o falso si no
        """
        portada = Portada.obtener_portada_album(id_album, Calidad.ORIGINAL)
        return portada is not None

    @staticmethod
    def validar_existe_portada_album(id_album, calidad):
        """
        Valida si existe la portada de un album
        :param id_album: El id del album a validar si tiene una portada registrada
        :param calidad: La calidad de la portada a validar si existe
        :return: Verdadero si existe la portada del album o falso si no
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        portada = Portada.obtener_portada_album(id_album, calidad)
        return portada is not None

    @staticmethod
    def convertir_formato_manejador_de_archivos_a_enum_formato(formato):
        """
        Convierte un enum ManejadorDeArchivos_pb2.FormatoImagen a enum FormatoImagen
        :param formato: El formato a convertir
        :return: El formato convertido
        """
        if formato == ManejadorDeArchivos_pb2.FormatoImagen.JPG:
            return FormatoImagen.JPG
        if formato == ManejadorDeArchivos_pb2.FormatoImagen.PNG:
            return FormatoImagen.PNG

    @staticmethod
    def guardar_portada_usuario(bytes_portada, id_usuario, formato, sha256):
        """
        Guarda la portada de un usuario en una ruta generada
        :param bytes_portada: Los bytes de la portada a guardar
        :param id_usuario: El id del usuario al que pertence la portada
        :param formato: El formato de la portada
        :param sha256: El hash256 de la portada
        :return: None
        """
        formato = ManejadorDePortadas.convertir_formato_manejador_de_archivos_a_enum_formato(formato)
        ruta_portada = ManejadorDeArchivos.guardar_portada_usuario(id_usuario, Calidad.ORIGINAL, formato, bytes_portada)
        alto = ManejadorDePortadas._obtener_alto_portada(ruta_portada)
        ancho = ManejadorDePortadas._obtener_ancho_portada(ruta_portada)
        portada = Portada.obtener_portada_usuario(id_usuario, Calidad.ORIGINAL)
        if portada is None:
            portada = Portada(id_usuario=id_usuario, es_original=True, calidad_imagen=Calidad.ORIGINAL,
                              ruta=ruta_portada, alto=alto, ancho=ancho, hash256=sha256, formato=formato)
            portada.guardar()
        else:
            portada.editar_portada(es_original=True, formato=formato, ruta=ruta_portada, hash256=sha256, ancho=ancho,
                                   alto=alto)
        ManejadorDePortadas.logger.info("Se ha gurdado la portada original del usuario con el id " + str(id_usuario))
        threading.Thread(target=ManejadorDePortadas.convertir_portada_todas_calidades, args=(id_usuario,
                                                                                             TipoPortada.USUARIO))

    @staticmethod
    def guardar_portada_creador_de_contenido(bytes_portada, id_creador_de_contenido, formato, sha256):
        """
        Guarda la portada de un creador de contenido en una ruta generada
        :param bytes_portada: Los bytes de la portada a guardar
        :param id_creador_de_contenido: El id del creador de contenido al que pertence la portada
        :param formato: El formato de la portada
        :param sha256: El hash256 de la portada
        :return: None
        """
        formato = ManejadorDePortadas.convertir_formato_manejador_de_archivos_a_enum_formato(formato)
        ruta_portada = ManejadorDeArchivos.guardar_portada_creador_de_contenido(id_creador_de_contenido,
                                                                                Calidad.ORIGINAL, formato,
                                                                                bytes_portada)
        alto = ManejadorDePortadas._obtener_alto_portada(ruta_portada)
        ancho = ManejadorDePortadas._obtener_ancho_portada(ruta_portada)
        portada = Portada.obtener_portada_creador_de_contenido(id_creador_de_contenido, Calidad.ORIGINAL)
        if portada is None:
            portada = Portada(id_creador_de_contenido=id_creador_de_contenido, es_original=True,
                              calidad_imagen=Calidad.ORIGINAL,
                              ruta=ruta_portada, alto=alto, ancho=ancho, hash256=sha256, formato=formato)
            portada.guardar()
        else:
            portada.editar_portada(es_original=True, formato=formato, ruta=ruta_portada, hash256=sha256, ancho=ancho,
                                   alto=alto)
        ManejadorDePortadas.logger.info("Se ha gurdado la portada original del creador de contenido con el id "
                                        + str(id_creador_de_contenido))
        threading.Thread(target=ManejadorDePortadas.convertir_portada_todas_calidades,
                         args=(id_creador_de_contenido, TipoPortada.CREADOR_DE_CONTENIDO))

    @staticmethod
    def guardar_portada_album(bytes_portada, id_album, formato, sha256):
        """
        Guarda la portada de un album en una ruta generada
        :param bytes_portada: Los bytes de la portada a guardar
        :param id_album: El id del album al que pertence la portada
        :param formato: El formato de la portada
        :param sha256: El hash256 de la portada
        :return: None
        """
        formato = ManejadorDePortadas.convertir_formato_manejador_de_archivos_a_enum_formato(formato)
        ruta_portada = ManejadorDeArchivos.guardar_portada_album(id_album, Calidad.ORIGINAL, formato, bytes_portada)
        alto = ManejadorDePortadas._obtener_alto_portada(ruta_portada)
        ancho = ManejadorDePortadas._obtener_ancho_portada(ruta_portada)
        portada = Portada.obtener_portada_album(id_album, Calidad.ORIGINAL)
        if portada is None:
            portada = Portada(id_album=id_album, es_original=True, calidad_imagen=Calidad.ORIGINAL,
                              ruta=ruta_portada, alto=alto, ancho=ancho, hash256=sha256, formato=formato)
            portada.guardar()
        else:
            portada.editar_portada(es_original=True, formato=formato, ruta=ruta_portada, hash256=sha256, ancho=ancho,
                                   alto=alto)
        ManejadorDePortadas.logger.info("Se ha gurdado la portada original del album con el id " + str(id_album))
        threading.Thread(target=ManejadorDePortadas.convertir_portada_todas_calidades, args=(id_album,
                                                                                             TipoPortada.ALBUM))

    @staticmethod
    def _obtener_alto_portada(ruta):
        """
        Obtiene el alto de la imagen que se encuentra en la ruta
        :param ruta: La ruta en donde se encuentra la imagen
        :return: El alto de la imagen
        """
        img = cv2.imread(ruta)
        height, width, channels = img.shape
        return height

    @staticmethod
    def _obtener_ancho_portada(ruta):
        """
        Obtiene el ancho de la imagen que se encuentra en la ruta
        :param ruta: La ruta en donde se encuentra la imagen
        :return: El ancho de la imagen
        """
        img = cv2.imread(ruta)
        height, width, channels = img.shape
        return width

    @staticmethod
    def convertir_portada_todas_calidades(id_elemento, tipo_portada):
        """
        Convierte una portada a todas sus calidades a PNG
        :param id_elemento: El id del elemento a convertir
        :param tipo_portada: El tipo de portada al que pertenece el id
        :return: None
        """
        cliente_convertidor = None
        mensaje_logger = ""
        if tipo_portada == TipoPortada.USUARIO:
            portada = Portada.obtener_portada_usuario(id_elemento, Calidad.ORIGINAL)
            cliente_convertidor = ConvertidorDeImagenesCliente(id_portada=portada.id_usuario,
                                                               ubicacion_archivo=portada.ruta,
                                                               extension=portada.formato.value)
            mensaje_logger = "Se ha mandado a convertir la portada del usuario con el id " + \
                             str(id_elemento) + " a todas sus calidades"
        elif tipo_portada == TipoPortada.CREADOR_DE_CONTENIDO:
            portada = Portada.obtener_portada_creador_de_contenido(id_elemento, Calidad.ORIGINAL)
            cliente_convertidor = ConvertidorDeImagenesCliente(id_portada=portada.id_creador_de_contenido,
                                                               ubicacion_archivo=portada.ruta,
                                                               extension=portada.formato.value)
            mensaje_logger = "Se ha mandado a convertir la portada del creador de contenido con el id " + \
                             str(id_elemento) + " a todas sus calidades"
        elif tipo_portada == TipoPortada.ALBUM:
            portada = Portada.obtener_portada_album(id_elemento, Calidad.ORIGINAL)
            cliente_convertidor = ConvertidorDeImagenesCliente(id_portada=portada.id_album,
                                                               ubicacion_archivo=portada.ruta,
                                                               extension=portada.formato.value)
            mensaje_logger = "Se ha mandado a convertir la portada del album con el id " + \
                             str(id_elemento) + " a todas sus calidades"
        cantidad_intentos = 0
        while cantidad_intentos < 3:
            try:
                ManejadorDePortadas.logger.info(mensaje_logger + ". Intento: " + str(cantidad_intentos))
                cliente_convertidor.enviar_imagen()
                ManejadorDePortadas._crear_portadas_convertidas(id_elemento, cliente_convertidor, tipo_portada)
                break
            except Exception as ex:
                ManejadorDePortadas.logger.error("Error convertir portada con el id " + str(id_elemento) + ": "
                                                 + str(ex))
                time.sleep(10)
                cantidad_intentos += 1

    @staticmethod
    def _crear_portadas_convertidas(id_elemento, cliente_convertidor, tipo_portada):
        """
        Se encarga de crear las tres Portada del id_elemento convertida en sus tres calidades
        :param id_elemento: El id del elemento convertido
        :param cliente_convertidor: El cliente del convertidor de imagenes que contiene las tres imagenes convertidas
        :return: None
        """
        ManejadorDePortadas._crear_portada_calidades(id_elemento, tipo_portada, cliente_convertidor,
                                                     Calidad.ALTA, FormatoImagen.PNG)
        ManejadorDePortadas._crear_portada_calidades(id_elemento, tipo_portada, cliente_convertidor,
                                                     Calidad.MEDIA, FormatoImagen.PNG)
        ManejadorDePortadas._crear_portada_calidades(id_elemento, tipo_portada, cliente_convertidor,
                                                     Calidad.BAJA, FormatoImagen.PNG)

    @staticmethod
    def _crear_portada_calidades(id_elemento, tipo_portada, cliente_convertidor, calidad, formato):
        """
        Crea una Portada con el id elemento
        :param id_elemento: El id del elemento que se convirtio
        :param cliente_convertidor: El cliente del convertidor de imagenes que contiene la informacion de las canciones
        convertidas
        :param calidad: La calidad de la Portada a guardar
        :param formato: El formato de la imagen personal
        :return: None
        """
        hash256 = ""
        ruta = ""
        if calidad == Calidad.BAJA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_baja.hash256
        elif calidad == Calidad.MEDIA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_media.hash256
        elif calidad == Calidad.ALTA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_alta.hash256
        if tipo_portada == TipoPortada.USUARIO:
            if calidad == Calidad.BAJA:
                ruta = ManejadorDeArchivos.guardar_portada_usuario(id_elemento, Calidad.BAJA, formato,
                                                                   cliente_convertidor.imagen_calidad_baja)
            if calidad == Calidad.MEDIA:
                ruta = ManejadorDeArchivos.guardar_portada_usuario(id_elemento, Calidad.MEDIA, formato,
                                                                   cliente_convertidor.imagen_calidad_media)
            if calidad == Calidad.ALTA:
                ruta = ManejadorDeArchivos.guardar_cancion_personal(id_elemento, Calidad.ALTA, formato,
                                                                    cliente_convertidor.imagen_calidad_alta)
            alto = ManejadorDePortadas._obtener_alto_portada(ruta)
            ancho = ManejadorDePortadas._obtener_ancho_portada(ruta)
            portada = Portada.obtener_portada_usuario(id_elemento, calidad)
            if portada is not None:
                portada.editar_portada(False, FormatoImagen.PNG, ruta, hash256, ancho, alto)
            else:
                portada = Portada(ruta, alto, ancho, hash256, FormatoImagen.PNG, calidad, id_usuario=id_elemento)
                portada.guardar()
        elif tipo_portada == TipoPortada.CREADOR_DE_CONTENIDO:
            if calidad == Calidad.BAJA:
                ruta = ManejadorDeArchivos.guardar_portada_creador_de_contenido(id_elemento, Calidad.BAJA, formato,
                                                                                cliente_convertidor.imagen_calidad_baja)
            if calidad == Calidad.MEDIA:
                ruta = ManejadorDeArchivos.guardar_portada_creador_de_contenido(id_elemento, Calidad.MEDIA, formato,
                                                                                cliente_convertidor.
                                                                                imagen_calidad_media)
            if calidad == Calidad.ALTA:
                ruta = ManejadorDeArchivos.guardar_portada_creador_de_contenido(id_elemento, Calidad.ALTA, formato,
                                                                                cliente_convertidor.imagen_calidad_alta)
            alto = ManejadorDePortadas._obtener_alto_portada(ruta)
            ancho = ManejadorDePortadas._obtener_ancho_portada(ruta)
            portada = Portada.obtener_portada_creador_de_contenido(id_elemento, calidad)
            if portada is not None:
                portada.editar_portada(False, FormatoImagen.PNG, ruta, hash256, ancho, alto)
            else:
                portada = Portada(ruta, alto, ancho, hash256, FormatoImagen.PNG, calidad,
                                  id_creador_de_contenido=id_elemento)
                portada.guardar()
        elif tipo_portada == TipoPortada.ALBUM:
            if calidad == Calidad.BAJA:
                ruta = ManejadorDeArchivos.guardar_portada_album(id_elemento, Calidad.BAJA, formato,
                                                                 cliente_convertidor.imagen_calidad_baja)
            if calidad == Calidad.MEDIA:
                ruta = ManejadorDeArchivos.guardar_portada_album(id_elemento, Calidad.MEDIA, formato,
                                                                 cliente_convertidor.imagen_calidad_media)
            if calidad == Calidad.ALTA:
                ruta = ManejadorDeArchivos.guardar_portada_album(id_elemento, Calidad.ALTA, formato,
                                                                 cliente_convertidor.imagen_calidad_alta)
            alto = ManejadorDePortadas._obtener_alto_portada(ruta)
            ancho = ManejadorDePortadas._obtener_ancho_portada(ruta)
            portada = Portada.obtener_portada_album(id_elemento, calidad)
            if portada is not None:
                portada.editar_portada(False, FormatoImagen.PNG, ruta, hash256, ancho, alto)
            else:
                portada = Portada(ruta, alto, ancho, hash256, FormatoImagen.PNG, calidad, id_album=id_elemento)
                portada.guardar()