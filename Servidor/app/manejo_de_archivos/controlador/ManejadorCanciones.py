import hashlib
import pathlib
import time

import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2

from app.manejo_de_archivos.modelo.enums.enums import Calidad
from app.manejo_de_archivos.modelo.modelos import ArchivoAudio

from Servidor.app.manejo_de_archivos.Cliente import ConvertidorDeArchivosCliente
from Servidor.app.manejo_de_archivos.controlador.ManejadorDeArchivos import ManejadorDeArchivos
from Servidor.app.manejo_de_archivos.modelo.enums.enums import FormatoAudio


class ManejadorCanciones:

    @staticmethod
    def guardar_cancion(informacion_cancion, bytes_de_la_cancion):
        pass

    @staticmethod
    def obtener_sha256_de_byte_array(array_de_bytes):
        hash256_cancion_calidad_alta = hashlib.sha3_256(array_de_bytes).hexdigest()
        return hash256_cancion_calidad_alta

    @staticmethod
    def validar_existe_cancion(id_cancion, calidad):
        if calidad == ManejadorDeArchivos_pb2.Calidad.ALTA:
            calidad = Calidad.ALTA
        elif calidad == ManejadorDeArchivos_pb2.Calidad.MEDIA:
            calidad = Calidad.MEDIA
        elif calidad == ManejadorDeArchivos_pb2.Calidad.BAJA:
            calidad = Calidad.BAJA
        archivo_cancion = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        return archivo_cancion is not None

    @staticmethod
    def validar_existe_archivo_cancion(id_cancion, calidad):
        if calidad == ManejadorDeArchivos_pb2.Calidad.ALTA:
            calidad = Calidad.ALTA
        elif calidad == ManejadorDeArchivos_pb2.Calidad.MEDIA:
            calidad = Calidad.MEDIA
        elif calidad == ManejadorDeArchivos_pb2.Calidad.BAJA:
            calidad = Calidad.BAJA
        archivo_cancion = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        if archivo_cancion is None:
            return None
        existe_archivo = ManejadorCanciones.validar_existe_archivo(archivo_cancion.ruta)
        return existe_archivo

    @staticmethod
    def validar_existe_cancion_original(id_cancion):
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        return archivo_audio is None

    @staticmethod
    def validar_existe_archivo_cancion_original(id_cancion):
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        if archivo_audio is None:
            return False
        existe_archivo_cancion = ManejadorCanciones.validar_existe_archivo(archivo_audio.ruta)
        return existe_archivo_cancion

    @staticmethod
    def validar_existe_archivo(ubicacion):
        archivo = pathlib.Path(ubicacion)
        return archivo.is_file()

    @staticmethod
    def reconvertir_cancion(id_cancion):
        archivo_cancion_original = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        cliente_convertidor = ConvertidorDeArchivosCliente(id_cancion=archivo_cancion_original.id_cancion,
                                                           ubicacion_archivo=archivo_cancion_original.ruta,
                                                           extension=archivo_cancion_original.formato.value)
        cantidad_intentos = 0
        while cantidad_intentos < 3:
            try:
                cliente_convertidor.enviar_cancion()
                ManejadorCanciones._crear_archivo_audio_canciones_convertidas(id_cancion, cliente_convertidor)
                break
            except Exception as ex:
                # Mostrar log
                time.sleep(10)
                cantidad_intentos += 1

    @staticmethod
    def _crear_archivo_audio_canciones_convertidas(id_cancion, cliente_convertidor):
        ManejadorCanciones._crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, Calidad.ALTA,
                                                                  FormatoAudio.MP3)
        ManejadorCanciones._crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, Calidad.MEDIA,
                                                                  FormatoAudio.MP3)
        ManejadorCanciones._crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, Calidad.BAJA,
                                                                  FormatoAudio.MP3)

    @staticmethod
    def _crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, calidad, formato):
        hash256 = ""
        tamano_cancion = 0
        ruta = ""
        if calidad == Calidad.BAJA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_baja.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_baja)
            ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.BAJA, formato,
                                                       cliente_convertidor.cancion_calidad_baja)
        elif calidad == Calidad.MEDIA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_media.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_media)
            ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.MEDIA, formato,
                                                       cliente_convertidor.cancion_calidad_media)
        elif calidad == Calidad.ALTA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_alta.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_alta)
            ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.ALTA, formato,
                                                       cliente_convertidor.cancion_calidad_alta)

        cancion_calidad = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        if cancion_calidad is None:
            cancion_calidad.editar_archivo_audio(False, FormatoAudio.MP3, ruta, hash256, tamano_cancion)
        else:
            cancion_calidad = ArchivoAudio(calidad, FormatoAudio.MP3, ruta, hash256, tamano_cancion,
                                           id_cancion=id_cancion)
            cancion_calidad.guardar()
