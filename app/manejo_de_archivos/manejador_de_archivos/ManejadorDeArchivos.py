import hashlib
import os

from app.manejo_de_archivos.modelo.enums.enums import Calidad
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2


class ManejadorDeArchivos:

    @staticmethod
    def guardar_cancion(id_cancion, calidad, formato, cancion):
        """
        Guarda una cancion en un ruta generada por el id_cancion y la calidad
        :param calidad: La calidad de la cancion a guardar
        :param id_cancion: El id de la cancion a guardar
        :param formato: El formato de la cancion
        :param cancion: Los bytes de la cancion a guardar
        :return: La ruta en donde se almaceno la cancion
        """
        ruta = ManejadorDeArchivos.crear_ruta_cancion(id_cancion, calidad)
        ruta_cancion = ruta + "/" + str(id_cancion) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_cancion, cancion)
        return ruta_cancion

    @staticmethod
    def crear_ruta_cancion(id_cancion, calidad):
        """
        Crea un direcotorio para almacenar una cancion en el lugar especifico
        :param id_cancion: El id de la cancion a guardar
        :param calidad: La calida de la cancion a guardar
        :return: La ruta generada
        """
        carpeta = "/canciones/" + str(id_cancion) + "/" + ManejadorDeArchivos._calcular_ruta_calidad(calidad)
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def _calcular_ruta_calidad(calidad):
        """
        Crea una cadena de texto a partir de la calidad
        :param calidad: La calidad a obtener su cadena de texto
        :return: Una cadena de texto
        """
        if calidad == Calidad.ALTA:
            return "alta"
        elif calidad == Calidad.MEDIA:
            return "media"
        elif calidad == Calidad.BAJA:
            return "baja"
        elif calidad == Calidad.ORIGINAL:
            return "original"

    @staticmethod
    def crear_ruta_cancion_personal(id_cancion, calidad):
        """
        Crea un direcotorio para almacenar una cancion personal en el lugar especifico
        :param id_cancion: El id de la cancion personal a guardar
        :param calidad: La calida de la cancion a guardar
        :return: La ruta generada
        """
        carpeta = "/canciones_personales/" + str(id_cancion) + "/" + \
                  ManejadorDeArchivos._calcular_ruta_calidad(calidad)

        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def guardar_portada_usuario(id_usuario, calidad, formato, portada):
        """
        Guarda la portada de un usuario en un directorio generado
        :param id_usuario: El id del usuario al que pertenece la portada
        :param calidad: La calidad de la portada
        :param formato: El formato de la portada
        :param portada: Los bytes de la portada
        :return: La ruta en donde se almaceno la portada
        """
        ruta = ManejadorDeArchivos.crear_ruta_portada_usuario(id_usuario, calidad)
        ruta_portada = ruta + "/" + str(id_usuario) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_portada, portada)
        return ruta_portada

    @staticmethod
    def guardar_portada_creador_de_contenido(id_creador_de_contenido, calidad, formato, portada):
        """
        Guarda la portada de un creador de contenido en un directorio generado
        :param id_creador_de_contenido: El id del creador de contenido al que pertenece la portada
        :param calidad: La calidad de la portada
        :param formato: El formato de la portada
        :param portada: Los bytes de la portada
        :return: La ruta en donde se almaceno la portada
        """
        ruta = ManejadorDeArchivos.crear_ruta_portada_creador_de_contenido(id_creador_de_contenido, calidad)
        ruta_portada = ruta + "/" + str(id_creador_de_contenido) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_portada, portada)
        return ruta_portada

    @staticmethod
    def guardar_portada_album(id_album, calidad, formato, portada):
        """
        Guarda la portada de un album en un directorio generado
        :param id_album: El id del album al que pertenece la portada
        :param calidad: La calidad de la portada
        :param formato: El formato de la portada
        :param portada: Los bytes de la portada
        :return: La ruta en donde se almaceno la portada
        """
        ruta = ManejadorDeArchivos.crear_ruta_portada_album(id_album, calidad)
        ruta_portada = ruta + "/" + str(id_album) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_portada, portada)
        return ruta_portada

    @staticmethod
    def crear_ruta_portada_usuario(id_usuario, calidad):
        """
        Crea un directorio para almacenar una portada de un usuario
        :param id_usuario: El id del usuario al que pertence la portada
        :param calidad: La calidad de la portada a guardar
        :return: La ruta del directorio creado
        """
        carpeta = "/portadas/usuarios/" + str(id_usuario) + "/" + ManejadorDeArchivos._calcular_ruta_calidad(calidad)
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def crear_ruta_portada_creador_de_contenido(id_creador_de_contenido, calidad):
        """
        Crea un directorio para almacenar una portada de un creador de contenido
        :param id_creador_de_contenido: El id del usuario al que pertence la portada
        :param calidad: La calidad de la portada a guardar
        :return: La ruta del directorio creado
        """
        carpeta = "/portadas/creadores-de-contenido/" + str(id_creador_de_contenido) + "/" +\
                  ManejadorDeArchivos._calcular_ruta_calidad(calidad)
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def crear_ruta_portada_album(id_album, calidad):
        """
        Crea un directorio para almacenar un album de un usuario
        :param id_album: El id del usuario al que pertence la portada
        :param calidad: La calidad de la portada a guardar
        :return: La ruta del directorio creado
        """
        carpeta = "/portadas/creadores-de-contenido/" + str(id_album) + "/" + \
                  ManejadorDeArchivos._calcular_ruta_calidad(calidad)
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def _escribir_archivo(ruta_archivo, archivo):
        """
        Escribe el archivo en la ruta_archivo
        :param ruta_archivo: La ruta en donde se almacenara el archivo
        :param archivo: El archivo a escribir
        :return: None
        """
        try:
            with open(ruta_archivo, 'wb') as f:
                f.write(archivo)
                f.close()
        except Exception as ex:
            print(ex)
        # Mostrar log de error

    @staticmethod
    def guardar_cancion_personal(id_cancion, formato, calidad, cancion):
        """
        Guarda una cancion personal en una reta generada
        :param id_cancion: El id de la cancion
        :param formato: El formato de la cancion
        :param calidad: La calidad de la cancion
        :param cancion: Los bytes de la cancion a guardar
        :return: La ruta en donde se guardo la cancion
        """
        ruta = ManejadorDeArchivos.crear_ruta_cancion_personal(id_cancion, calidad)
        ruta_cancion = ruta + "/" + str(id_cancion) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_cancion, cancion)
        return ruta_cancion

    @staticmethod
    def convertir_calidad_proto_a_calidad_enum(calidad):
        """
        Convierte un enum ManejadorDeArchivos_pb2 a un enum Calidad
        :param calidad: La calidad a convertir
        :return: Un enum Calidad
        """
        if calidad == ManejadorDeArchivos_pb2.Calidad.ALTA:
            return Calidad.ALTA
        elif calidad == ManejadorDeArchivos_pb2.Calidad.MEDIA:
            return Calidad.MEDIA
        elif calidad == ManejadorDeArchivos_pb2.Calidad.BAJA:
            return Calidad.BAJA

    @staticmethod
    def obtener_sha256_de_byte_array(array_de_bytes):
        """
        Calcula el hash del arreglo de bytes con el algoritmo sha256
        :param array_de_bytes: El arreglo de bytes a calcular el hash
        :return: Un string con el hash256 del arreglo de bytes
        """
        hash256 = hashlib.sha3_256(array_de_bytes).hexdigest()
        return hash256
