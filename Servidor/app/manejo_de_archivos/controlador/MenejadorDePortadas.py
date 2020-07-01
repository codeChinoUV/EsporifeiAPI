from app.manejo_de_archivos.modelo.modelos import Portada
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import Calidad
from app.manejo_de_archivos.controlador.ManejadorDeArchivos import ManejadorDeArchivos
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2
from app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 import FormatoImagen
import cv2


class ManejadorDePortadas:

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
