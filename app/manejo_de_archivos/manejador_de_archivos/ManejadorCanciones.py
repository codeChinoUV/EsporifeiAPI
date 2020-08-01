import logging
import pathlib
import time

import app.manejo_de_archivos.protos.ManejadorDeArchivos_pb2 as ManejadorDeArchivos_pb2
import eyed3

from app.administracion_de_contenido.controlador.v1.BibliotecaPersonalControlador import BibliotecaPersonalCanciones
from app.administracion_de_contenido.controlador.v1.CancionesControlador import CreadorDeContenidoAlbumCancion
from app.manejo_de_archivos.manejador_de_archivos.ManejadorDeArchivos import ManejadorDeArchivos
from app.manejo_de_archivos.modelo.enums.enums import Calidad
from app.manejo_de_archivos.modelo.modelos import ArchivoAudio
from app.manejo_de_archivos.modelo.enums.enums import FormatoAudio
from pydub import AudioSegment
from app.manejo_de_archivos.clientes_convertidor_archivos.ClienteConvertidorCanciones import \
    ConvertidorDeCancionesCliente


class ManejadorCanciones:
    logger = logging.getLogger()

    @staticmethod
    def guardar_cancion(bytes_de_la_cancion, id_cancion, formato):
        """
        Crea el archivo de la cancion y un ArchivoAudio con la informacion de la canciion
        :param bytes_de_la_cancion: Los bytes de la cancion a guardar
        :param id_cancion: El id de la cancion a la cual pertenecera la cancion
        :param formato: El formato de la cancion
        :return: None
        """
        if formato == ManejadorDeArchivos_pb2.FormatoAudio.MP3:
            formato = FormatoAudio.MP3
        elif formato == ManejadorDeArchivos_pb2.FormatoAudio.FLAC:
            formato = FormatoAudio.FLAC
        elif formato == ManejadorDeArchivos_pb2.M4A:
            formato = FormatoAudio.M4A
        tamano = len(bytes_de_la_cancion)
        ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.ORIGINAL, formato, bytes_de_la_cancion)
        CreadorDeContenidoAlbumCancion.modificar_duracion(id_cancion,
                                                          ManejadorCanciones._obtener_duracion_cancion(ruta))
        archivo_de_audio = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        hash256 = ManejadorDeArchivos.obtener_sha256_de_byte_array(bytes_de_la_cancion)
        if archivo_de_audio is None:
            archivo_audio = ArchivoAudio(Calidad.ORIGINAL, formato, ruta, hash256, tamano, id_cancion=id_cancion,
                                         es_original=True)
            archivo_audio.guardar()
        else:
            archivo_de_audio.editar_archivo_audio(es_original=True, formato=formato, ruta=ruta, hash256=hash256,
                                                  tamano=tamano)
        ManejadorCanciones.logger.info("Se ha gurdado la cancion original con el id " + str(id_cancion))
        from app.manejo_de_archivos.clientes_convertidor_archivos.ConvertidorDeArchivos import ConvertidorDeArchivos
        convertidor_de_archivos = ConvertidorDeArchivos()
        convertidor_de_archivos.agregar_cancion_a_cola(id_cancion)

    @staticmethod
    def _obtener_duracion_cancion(ruta):
        """
        Obtiene la duracion en segundos de un archivo
        :param ruta: La ruta en donde se encuentra el archivo
        :return: Un flotante con la duracion en segundos
        """
        cancion = AudioSegment.from_file("./" + ruta, channels=2)
        return cancion.duration_seconds

    @staticmethod
    def validar_existe_cancion(id_cancion, calidad):
        """
        Valida si se encuentra registrado el ArchivoAudio de la cancion con el id_cancion en la calidad
        :param id_cancion: El id de la cancion
        :param calidad: La calidad de la cancion
        :return: True si se encuentra registrada o False si no
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        archivo_cancion = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        return archivo_cancion is not None

    @staticmethod
    def validar_existe_archivo_cancion(id_cancion, calidad):
        """
        Valida si el archivo de la cancion con el id cancion existe
        :param id_cancion: El id de la cancion a validar si su archivo existe
        :param calidad: La calidad de la cancion
        :return: True si existe o false si no
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        archivo_cancion = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        if archivo_cancion is None:
            return None
        existe_archivo = ManejadorCanciones.validar_existe_archivo(archivo_cancion.ruta)
        return existe_archivo

    @staticmethod
    def validar_existe_cancion_original(id_cancion):
        """
        Valida si existe el ArchivoAudio de la cancion original en la base de datos
        :param id_cancion: El id de la cancion a validar si existe su ArchivoAudio
        :return: True si existe o False si no
        """
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        existe = False
        if archivo_audio is not None:
            existe = ManejadorDeArchivos.validar_existe_archivo(archivo_audio.ruta)
        return archivo_audio is not None and existe

    @staticmethod
    def validar_existe_archivo_cancion_original(id_cancion):
        """
        Valida si existe el archivo de la cancion original
        :param id_cancion: El id de la cancion a validar si existe su archivo
        :return: True si existe o False si no
        """
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        if archivo_audio is None:
            return False
        existe_archivo_cancion = ManejadorCanciones.validar_existe_archivo(archivo_audio.ruta)
        return existe_archivo_cancion

    @staticmethod
    def validar_existe_archivo(ubicacion):
        """
        Valida si existe un archivo en la ubicacion indicada
        :param ubicacion: La ubicacion en donde se buscara el archivo
        :return: True si el archivo existe o False si no
        """
        archivo = pathlib.Path(ubicacion)
        return archivo.is_file()

    @staticmethod
    def convertir_cancion_wav_todas_calidades(id_cancion):
        """
        Se encarga de reconvertir la cancion con el id cancion a mp3 en todas sus calidades
        :param id_cancion: El id de la cancion a reconvertir
        :return: None
        """
        archivo_cancion_original = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, Calidad.ORIGINAL)
        id_cancion_str = str(archivo_cancion_original.id_cancion) + "C"
        cliente_convertidor = ConvertidorDeCancionesCliente(id_cancion=id_cancion_str,
                                                            ubicacion_archivo=archivo_cancion_original.ruta,
                                                            extension=archivo_cancion_original.formato.value)
        cantidad_intentos = 1
        while cantidad_intentos <= 3:
            try:
                ManejadorCanciones.logger.info("Se ha mandado a convertir la cancion con el id " +
                                               str(id_cancion) + " a todas sus calidades. Intento: "
                                               + str(cantidad_intentos))
                cliente_convertidor.enviar_archivo()
                ManejadorCanciones._crear_archivo_audio_canciones_convertidas(id_cancion, cliente_convertidor)
                break
            except Exception as ex:
                ManejadorCanciones.logger.error("Error convertir cancion con el id " + str(id_cancion) + ": "
                                                + str(ex))
                time.sleep(10)
                cantidad_intentos += 1

    @staticmethod
    def _crear_archivo_audio_canciones_convertidas(id_cancion, cliente_convertidor):
        """
        Se encarga de crear los tres ArchivoAudio de la cancion convertida en sus tres calidades
        :param id_cancion: El id de la cancion convertida
        :param cliente_convertidor: El cliente del convertidor de archivos que contiene las tres canciones convertidas
        :return: None
        """
        ManejadorCanciones._crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, Calidad.ALTA,
                                                                  FormatoAudio.MP3)
        ManejadorCanciones._crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, Calidad.MEDIA,
                                                                  FormatoAudio.MP3)
        ManejadorCanciones._crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, Calidad.BAJA,
                                                                  FormatoAudio.MP3)

    @staticmethod
    def _crear_archivo_audio_cancion_calidades(id_cancion, cliente_convertidor, calidad, formato):
        """
        Crea un ArchivoAudio de la cancion
        :param id_cancion: El id de la cancion que se convirtio
        :param cliente_convertidor: El cliente del convertidor de archivos que contiene la informacion de las canciones
        convertidas
        :param calidad: La calidad del ArchivoAudio a guardar
        :param formato: El formato de la cancion
        :return: None
        """
        hash256 = ""
        tamano_cancion = 0
        ruta = ""
        calidad_str = ""
        if calidad == Calidad.BAJA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_baja.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_baja)
            ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.BAJA, formato,
                                                       cliente_convertidor.cancion_calidad_baja)
            calidad_str = "baja"
        elif calidad == Calidad.MEDIA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_media.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_media)
            ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.MEDIA, formato,
                                                       cliente_convertidor.cancion_calidad_media)
            calidad_str = "media"
        elif calidad == Calidad.ALTA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_alta.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_alta)
            ruta = ManejadorDeArchivos.guardar_cancion(id_cancion, Calidad.ALTA, formato,
                                                       cliente_convertidor.cancion_calidad_alta)
            calidad_str = "alta"
        cancion_calidad = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        if cancion_calidad is not None:
            cancion_calidad.editar_archivo_audio(False, formato, ruta, hash256, tamano_cancion)
        else:
            cancion_calidad = ArchivoAudio(calidad, formato, ruta, hash256, tamano_cancion,
                                           id_cancion=id_cancion)
            cancion_calidad.guardar()
        ManejadorCanciones.logger.info("Se ha gurdado la cancion en calidad " + calidad_str + " con el id " +
                                       str(id_cancion))

    @staticmethod
    def guardar_cancion_personal(bytes_de_la_cancion, id_cancion, formato):
        """
        Crea el archivo de la cancion personal y un ArchivoAudio con la informacion de la cancion personal
        :param bytes_de_la_cancion: Los bytes de la cancion a guardar
        :param id_cancion: El id de la cancion a la cual pertenecera la cancion
        :param formato: El formato de la cancion
        :return: None
        """
        if formato == ManejadorDeArchivos_pb2.FormatoAudio.MP3:
            formato = FormatoAudio.MP3
        elif formato == ManejadorDeArchivos_pb2.FormatoAudio.FLAC:
            formato = FormatoAudio.FLAC
        elif formato == ManejadorDeArchivos_pb2.M4A:
            formato = FormatoAudio.M4A
        tamano = len(bytes_de_la_cancion)
        ruta = ManejadorDeArchivos.guardar_cancion_personal(id_cancion, formato, Calidad.ORIGINAL, bytes_de_la_cancion)
        BibliotecaPersonalCanciones.modificar_duracion(id_cancion, ManejadorCanciones._obtener_duracion_cancion(ruta))
        archivo_de_audio = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, Calidad.ORIGINAL)
        hash256 = ManejadorDeArchivos.obtener_sha256_de_byte_array(bytes_de_la_cancion)
        if archivo_de_audio is None:
            archivo_audio = ArchivoAudio(Calidad.ORIGINAL, formato, ruta, hash256, tamano,
                                         id_cancion_personal=id_cancion, es_original=True)
            archivo_audio.guardar()
        else:
            archivo_de_audio.editar_archivo_audio(es_original=True, formato=formato, ruta=ruta, hash256=hash256,
                                                  tamano=tamano)
        ManejadorCanciones.logger.info("Se ha gurdado la cancion personal original con el id " + str(id_cancion))
        from app.manejo_de_archivos.clientes_convertidor_archivos.ConvertidorDeArchivos import ConvertidorDeArchivos
        convertidor_de_archivos = ConvertidorDeArchivos()
        convertidor_de_archivos.agregar_cancion_personal_a_cola(id_cancion)

    @staticmethod
    def validar_existe_cancion_personal_original(id_cancion):
        """
        Se encarga de validar si existe el ArchivoAudio con el id_cancion_personal
        :param id_cancion: El id de la cancion personal a validar si existe
        :return: True si el ArchivoAudio de la cancion personal con la calidad ORIGINAL o False si no
        """
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, Calidad.ORIGINAL)
        existe = False
        if archivo_audio is not None:
            existe = ManejadorDeArchivos.validar_existe_archivo(archivo_audio.ruta)
        return archivo_audio is not None and existe

    @staticmethod
    def validar_existe_archivo_cancion_personal_original(id_cancion):
        """
        Se encarga de validar si el archico de la cancion personal con el id existe
        :param id_cancion: El id cancion personal a validar si existe su archivo
        :return: True si existe el archivo o False si no
        """
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, Calidad.ORIGINAL)
        if archivo_audio is None:
            return False
        existe_archivo_cancion = ManejadorCanciones.validar_existe_archivo(archivo_audio.ruta)
        return existe_archivo_cancion

    @staticmethod
    def validar_existe_cancion_personal(id_cancion, calidad):
        """
        Valida si existe el ArchivoAudio de una cancion personal con la calidad indicada
        :param id_cancion: El id de la cancion personal a validar si existe
        :param calidad: La caliad del ArchivoAudio a validar si existe
        :return: True si existe el ArchivoAudio de la cancion personal con la calidad indicada
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        archivo_cancion = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, calidad)
        return archivo_cancion is not None

    @staticmethod
    def validar_existe_archivo_cancion_personal(id_cancion, calidad):
        """
        Se encarga de validar si el archico de la cancion personal con el id y la calidad indicada existe
        :param id_cancion: El id cancion personal a validar si existe su archivo
        :param calidad: La calidad de la cancion a validar si existe su archivo
        :return: True si existe el archivo o False si no
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        archivo_cancion = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, calidad)
        if archivo_cancion is None:
            return None
        existe_archivo = ManejadorCanciones.validar_existe_archivo(archivo_cancion.ruta)
        return existe_archivo

    @staticmethod
    def convertir_cancion_personal_wav_todas_calidades(id_cancion):
        """
        Reconvierte una cancion personal a mp3 en todas las calidades
        :param id_cancion: El id de la cancion personal a reconvertir el archivo a todas sus calidades
        :return: None
        """
        archivo_cancion_original = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, Calidad.ORIGINAL)
        id_cancion_personal_str = str(archivo_cancion_original.id_cancion_personal) + "CP"
        cliente_convertidor = ConvertidorDeCancionesCliente(id_cancion=id_cancion_personal_str,
                                                            ubicacion_archivo=archivo_cancion_original.ruta,
                                                            extension=archivo_cancion_original.formato.value)
        cantidad_intentos = 0
        while cantidad_intentos < 3:
            try:
                ManejadorCanciones.logger.info("Se ha mandado a convertir la cancion personal con el id " +
                                               str(id_cancion) + " a todas sus calidades. Intento: "
                                               + str(cantidad_intentos))
                cliente_convertidor.enviar_archivo()
                ManejadorCanciones._crear_archivo_audio_canciones_personales_convertidas(id_cancion,
                                                                                         cliente_convertidor)
                break
            except Exception as ex:
                ManejadorCanciones.logger.error("Error convertir cancion personal con el id " + str(id_cancion) + ": "
                                                + str(ex))
                time.sleep(10)
                cantidad_intentos += 1

    @staticmethod
    def _colocar_metadata_cancion_personal(cancion_personal, ruta):
        """
        Coloca la informacion de la cancion personal al archivo
        :param ruta: La ruta en donde se encuentra el archivo de la cancion personal
        :param cancion_personal: La cancion personal con la informacion de la cancion
        :return: None
        """
        archivo_de_audio = eyed3.load(ruta)
        archivo_de_audio.tag.artist = cancion_personal.artistas
        archivo_de_audio.tag.album = cancion_personal.album
        archivo_de_audio.tag.title = cancion_personal.nombre
        archivo_de_audio.tag.save()

    @staticmethod
    def _crear_archivo_audio_canciones_personales_convertidas(id_cancion, cliente_convertidor):
        """
        Se encarga de crear los tres ArchivoAudio de la cancion personal convertida en sus tres calidades
        :param id_cancion: El id de la cancion personal convertida
        :param cliente_convertidor: El cliente del convertidor de archivos que contiene las tres canciones personales
        convertidas
        :return: None
        """
        ManejadorCanciones._crear_archivo_audio_cancion_personal_calidades(id_cancion, cliente_convertidor,
                                                                           Calidad.ALTA, FormatoAudio.MP3)
        ManejadorCanciones._crear_archivo_audio_cancion_personal_calidades(id_cancion, cliente_convertidor,
                                                                           Calidad.MEDIA, FormatoAudio.MP3)
        ManejadorCanciones._crear_archivo_audio_cancion_personal_calidades(id_cancion, cliente_convertidor,
                                                                           Calidad.BAJA, FormatoAudio.MP3)

    @staticmethod
    def _crear_archivo_audio_cancion_personal_calidades(id_cancion, cliente_convertidor, calidad, formato):
        """
        Crea un ArchivoAudio de la cancion personal
        :param id_cancion: El id de la cancion personal que se convirtio
        :param cliente_convertidor: El cliente del convertidor de archivos que contiene la informacion de las canciones
        convertidas
        :param calidad: La calidad del ArchivoAudio a guardar
        :param formato: El formato de la cancion personal
        :return: None
        """
        hash256 = ""
        tamano_cancion = 0
        ruta = ""
        calidad_str = ""
        if calidad == Calidad.BAJA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_baja.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_baja)
            ruta = ManejadorDeArchivos.guardar_cancion_personal(id_cancion, formato, Calidad.BAJA,
                                                                cliente_convertidor.cancion_calidad_baja)
            calidad_str = "baja"
        elif calidad == Calidad.MEDIA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_media.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_media)
            ruta = ManejadorDeArchivos.guardar_cancion_personal(id_cancion, formato, Calidad.MEDIA,
                                                                cliente_convertidor.cancion_calidad_media)
            calidad_str = "meadia"
        elif calidad == Calidad.ALTA:
            hash256 = cliente_convertidor.informacion_archivo_calidad_alta.hash256
            tamano_cancion = len(cliente_convertidor.cancion_calidad_alta)
            ruta = ManejadorDeArchivos.guardar_cancion_personal(id_cancion, formato, Calidad.ALTA,
                                                                cliente_convertidor.cancion_calidad_alta)
            calidad_str = "alta"
        cancion_calidad = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion, calidad)
        if cancion_calidad is not None:
            cancion_calidad.editar_archivo_audio(False, formato, ruta, hash256, tamano_cancion)
        else:
            cancion_calidad = ArchivoAudio(calidad, formato, ruta, hash256, tamano_cancion,
                                           id_cancion_personal=id_cancion)
            cancion_calidad.guardar()
        ManejadorCanciones.logger.info("Se ha gurdado la cancion personal en calidad " + calidad_str + " con el id " +
                                       str(id_cancion))

    @staticmethod
    def obtener_archivo_audio_cancion(id_cancion, calidad):
        """
        Recupera el archivo de audio de la cancion con la calidad indicada
        :param id_cancion: El id de la cancion a recuperar
        :param calidad: La calidad de la cancion a recuperar
        :return: Un ArchivoAudio
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion(id_cancion, calidad)
        return archivo_audio

    @staticmethod
    def obtener_archivo_audio_cancion_personal(id_cancion_personal, calidad):
        """
        Recupera el archivo de audio de la cancionPersonal con la calidad indicada
        :param id_cancion_personal: El id de la cancionPersonal a recuperar
        :param calidad: La calidad de la cancionPersonal a recuperar
        :return: Un ArchivoAudio
        """
        calidad = ManejadorDeArchivos.convertir_calidad_proto_a_calidad_enum(calidad)
        archivo_audio = ArchivoAudio.obtener_archivo_audio_cancion_personal(id_cancion_personal, calidad)
        return archivo_audio
