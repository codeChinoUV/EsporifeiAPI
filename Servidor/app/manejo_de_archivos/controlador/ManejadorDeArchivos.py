import os

from app.manejo_de_archivos.modelo.enums.enums import Calidad
from app.manejo_de_archivos.protos import ManejadorDeArchivos_pb2


class ManejadorDeArchivos:

    @staticmethod
    def guardar_cancion(id_cancion, calidad, formato, cancion):
        ruta = ManejadorDeArchivos.crear_ruta_cancion(id_cancion, calidad)
        ruta_cancion = ruta + "/" + str(id_cancion) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_cancion, cancion)
        return ruta_cancion

    @staticmethod
    def crear_ruta_cancion(id_cancion, calidad):
        carpeta = "/canciones/" + str(id_cancion) + "/" + ManejadorDeArchivos._calcular_ruta_calidad(calidad)
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def _calcular_ruta_calidad(calidad):
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
        carpeta = "/canciones_personales/" + str(id_cancion) + "/" + \
                  ManejadorDeArchivos._calcular_ruta_calidad(calidad)

        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def _escribir_archivo(ruta_archivo, archivo):
        try:
            with open(ruta_archivo, 'wb') as f:
                f.write(archivo)
                f.close()
        except Exception as ex:
            print(ex)
        # Mostrar log de error

    @staticmethod
    def guardar_cancion_personal(id_cancion, formato, calidad, cancion):
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