import os

from Servidor.app.manejo_de_archivos.modelo.enums.enums import Calidad


class ManejadorDeArchivos:

    @staticmethod
    def guardar_cancion(id_cancion, calidad, formato, cancion):
        ruta = ManejadorDeArchivos.crear_ruta_cancion(id_cancion, calidad)
        ruta_cancion = ruta + "/" + str(id_cancion) + "." + formato.value
        ManejadorDeArchivos._escribir_archivo(ruta_cancion, cancion)
        return ruta_cancion

    @staticmethod
    def crear_ruta_cancion(id_cancion, calidad):
        carpeta = "/canciones/" + str(id_cancion) + "/"
        if calidad == Calidad.ALTA:
            carpeta += "alta"
        elif calidad == Calidad.MEDIA:
            carpeta += "media"
        elif calidad == Calidad.BAJA:
            carpeta += "baja"
        elif calidad == Calidad.ORIGINAL:
            carpeta += "original"
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    @staticmethod
    def crear_ruta_cancion_personal(id_cancion, calidad):
        carpeta = "/canciones_personales/" + str(id_cancion) + "/"
        if calidad == Calidad.ALTA:
            carpeta += "alta"
        elif calidad == Calidad.MEDIA:
            carpeta += "media"
        elif calidad == Calidad.BAJA:
            carpeta += "baja"
        elif calidad == Calidad.ORIGINAL:
            carpeta += "original"
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