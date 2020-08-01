import hashlib
import pathlib

from pydub import AudioSegment
from os import remove


class ConvertidorDeCanciones:
    CALIDAD_ALTA = "320k"
    CALIDAD_MEDIA = "256k"
    CALIDAD_BAJA = "128k"
    CALIDAD_ORIGINAL = "original"
    FORMATO_MP3 = "mp3"
    TAMANO_CHUNK = 1000 * 64

    def __init__(self, logger):
        self.logger = logger
        self.id_cancion = 0
        self.ubicacion_fichero = None
        self.ubicacion_fichero_calidad_alta = None
        self.ubicacion_fichero_calidad_media = None
        self.ubicacion_fichero_calidad_baja = None

    def convertir_a_wav_calidad_alta(self):
        """
        Convierte la cancion original a mp3 a 320kbs
        :return: El lugar en donde se guardo el archivo
        """
        self.logger.info("Se empezo a convertir la cancion con el id " + str(self.id_cancion) + " a mp3 calidad alta")
        self.ubicacion_fichero_calidad_alta = self._convetir_cancion(ConvertidorDeCanciones.CALIDAD_ALTA)
        self.logger.info("Se convirtio la cancion con el id " + str(self.id_cancion) + " a mp3 en calidad alta")
        return self.ubicacion_fichero_calidad_alta

    def convertir_a_wav_calidad_media(self):
        """
        Convierte la cancion original a mp3 a 256kbs
        :return: El lugar en donde se guardo el archivo
        """
        self.logger.info("Se empezo a convertir la cancion con el id " + str(self.id_cancion) + " a mp3 calidad media")
        self.ubicacion_fichero_calidad_media = self._convetir_cancion(ConvertidorDeCanciones.CALIDAD_MEDIA)
        self.logger.info("Se convirtio la cancion con el id " + str(self.id_cancion) + " a mp3 en calidad media")
        return self.ubicacion_fichero_calidad_media

    def convertir_a_mp3_calidad_baja(self):
        """
        Convierte la cancion original a mp3 a 128kbs
        :return: El lugar en donde se guardo el archivo
        """
        self.logger.info("Se empezo a convertir la cancion con el id " + str(self.id_cancion) + " a mp3 calidad baja")
        self.ubicacion_fichero_calidad_baja = self._convetir_cancion(ConvertidorDeCanciones.CALIDAD_BAJA)
        self.logger.info("Se convirtio la cancion con el id " + str(self.id_cancion) + " a mp3 en calidad baja")
        return self.ubicacion_fichero_calidad_baja

    def _convetir_cancion(self, calidad):
        """
        Se encarga de convertir la cancion original a mp3 a la calidad indicada
        :param calidad: La calidad la cual tendra el archivo convertido
        :return: La ubicacion en donde se guardo el archivo
        """
        try:
            cancion = AudioSegment.from_file(self.ubicacion_fichero, channels=2)
            ruta_cancion = str(self.id_cancion) + calidad + "." + ConvertidorDeCanciones.FORMATO_MP3
            cancion.export(ruta_cancion, format=ConvertidorDeCanciones.FORMATO_MP3, bitrate=calidad)
            return ruta_cancion
        except Exception as ex:
            self.logger.info("excepcion: " + str(ex))

    def escribir_fichero(self, id_cancion, extension, arreglo_de_bytes):
        """
        Escribe en un archivo el arreglo de bytes para poder llevar a cabo su transformacion
        :param id_cancion: El id que tiene la cancion en la base de datos
        :param extension: La extension original del archivo
        :param arreglo_de_bytes: Los bytes que contiene el archivo
        :return: La ubicacion en donde se guardo el achivo
        """
        self.id_cancion = str(id_cancion)
        self.ubicacion_fichero = '/tmp/' + str(id_cancion) + '.' + extension
        archivo = pathlib.Path(self.ubicacion_fichero)
        try:
            if not archivo.is_file():
                with open(self.ubicacion_fichero, 'wb') as f:
                    f.write(arreglo_de_bytes)
                    f.close()
            else:
                with open(self.ubicacion_fichero, 'ab') as f:
                    f.write(arreglo_de_bytes)
                    f.close()
        except Exception as ex:
            print(ex)

    @staticmethod
    def leer_archivo_binario(ruta):
        """
        Lee el archivo que se encuentra en la ruta y devulve un arreglo de bytes del archivo
        :param ruta: La ruta del archivo a leer
        :return: Un arreglo de bytes o None si no se encuentra el archivo
        """
        try:
            with open(ruta, mode='rb') as archivo:
                cancion = archivo.read()
                archivo.close()
            return cancion
        except FileNotFoundError:
            return None

    @staticmethod
    def eliminar_archivo(ruta_archivo):
        """
        Elimina el archivo que este en la ruta seleccionada
        :param ruta_archivo: La ruta del archivo a eliminar
        :return: None
        """
        remove(ruta_archivo)

    def limpiar_archivos(self):
        """
        Elimina todos los archivos generados al momento de transformar la cancion
        :return: None
        """
        try:
            if self.ubicacion_fichero is not None:
                ConvertidorDeCanciones.eliminar_archivo(self.ubicacion_fichero)
                ConvertidorDeCanciones.eliminar_archivo(self.ubicacion_fichero_calidad_alta)
                ConvertidorDeCanciones.eliminar_archivo(self.ubicacion_fichero_calidad_media)
                ConvertidorDeCanciones.eliminar_archivo(self.ubicacion_fichero_calidad_baja)
        except FileNotFoundError:
            print("No se encontraron los archivos a limpiar")

    def obtener_sha256_de_cancion_original(self):
        """
        Obtiene el hash256 del archivo original
        :return: El hash256 del archivo original
        """
        hash256 = hashlib.sha3_256()
        with open(self.ubicacion_fichero, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(ConvertidorDeCanciones.TAMANO_CHUNK), b""):
                hash256.update(bloque)
        return hash256.hexdigest()
