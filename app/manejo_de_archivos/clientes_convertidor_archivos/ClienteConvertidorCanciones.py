import pathlib

import grpc
import hashlib

from app.manejo_de_archivos.protos_convertidor_de_archivos import ConvertidorDeArchivos_pb2


class ConvertidorDeCancionesCliente:

    def __init__(self, id_cancion, ubicacion_archivo, extension):
        self.id_cancion = id_cancion
        self.extension = extension
        # Tamaño de 64 Kb
        self.tamano_chunk = 1000 * 64
        self.ubicacion_archivo = ubicacion_archivo
        self.informacion_archivo = ConvertidorDeArchivos_pb2.InformacionArchivo()
        self.cancion_calidad_alta = bytearray()
        self.informacion_archivo_calidad_alta = None
        self.cancion_calidad_media = bytearray()
        self.informacion_archivo_calidad_media = None
        self.cancion_calidad_baja = bytearray()
        self.informacion_archivo_calidad_baja = None
        self.error = None

    def _validar_existe_archivo(self):
        archivo = pathlib.Path(self.ubicacion_archivo)
        if not archivo.is_file():
            error = ConvertidorDeArchivos_pb2.ErrorGeneral()
            error.error = "archivo_no_existe"
            error.mensaje = "El archivo no existe en la ruta indicada"
            return error

    def _obtener_sha256(self, ubicacion_archivo):
        hash256 = hashlib.sha3_256()
        with open(ubicacion_archivo, 'rb') as archivo:
            for bloque in iter(lambda: archivo.read(self.tamano_chunk), b""):
                hash256.update(bloque)
        return hash256.hexdigest()

    def _validar_sha256_de_canciones_recibidas(self):
        hash256_cancion_calidad_alta = hashlib.sha3_256(self.cancion_calidad_alta).hexdigest()
        hash256_cancion_calidad_media = hashlib.sha3_256(self.cancion_calidad_media).hexdigest()
        hash256_cancion_calidad_baja = hashlib.sha3_256(self.cancion_calidad_baja).hexdigest()
        return hash256_cancion_calidad_alta == self.informacion_archivo_calidad_alta.hash256 and \
               hash256_cancion_calidad_media == self.informacion_archivo_calidad_media.hash256 and \
               hash256_cancion_calidad_baja == self.informacion_archivo_calidad_baja.hash256

    def enviar_cancion(self):
        with open(self.ubicacion_archivo, 'rb') as archivo:
            solicitud = ConvertidorDeArchivos_pb2.SolicitudConvertirCancionMp3()
            solicitud.informacionArchivo.idCancion = int(self.id_cancion)
            solicitud.informacionArchivo.extension = self.extension
            solicitud.informacionArchivo.hash256 = self.informacion_archivo.hash256
            for bloque in iter(lambda: archivo.read(self.tamano_chunk), b""):
                solicitud.paquete.data = bloque
                yield solicitud

    def recibir_cancion(self, respuesta):
        if respuesta.error.error != "":
            self.error = respuesta.error
        if len(respuesta.cancionCalidadAlta.paquete.data) > 0:
            self.cancion_calidad_alta += bytearray(respuesta.cancionCalidadAlta.paquete.data)
            if respuesta.cancionCalidadAlta.informacionArchivo is not None:
                self.informacion_archivo_calidad_alta = respuesta.cancionCalidadAlta.informacionArchivo
        if len(respuesta.cancionCalidadMedia.paquete.data) > 0:
            self.cancion_calidad_media += bytearray(respuesta.cancionCalidadMedia.paquete.data)
            if respuesta.cancionCalidadAlta.informacionArchivo is not None:
                self.informacion_archivo_calidad_media = respuesta.cancionCalidadMedia.informacionArchivo
        if len(respuesta.cancionCalidadBaja.paquete.data) > 0:
            self.cancion_calidad_baja += bytearray(respuesta.cancionCalidadBaja.paquete.data)
            if respuesta.cancionCalidadBaja.informacionArchivo is not None:
                self.informacion_archivo_calidad_baja = respuesta.cancionCalidadBaja.informacionArchivo

    def enviar_archivo(self):
        canal = grpc.insecure_channel('192.168.0.15:5002')
        cliente = ConvertidorDeArchivos_pb2_grpc.ConvertidorDeCancionesStub(canal)
        existe_el_archivo = self._validar_existe_archivo()
        if existe_el_archivo is not None:
            return existe_el_archivo
        self.informacion_archivo.hash256 = self._obtener_sha256(self.ubicacion_archivo)
        cantidad_intentos = 0
        # Valida si no ocurrio un error al convertir la cancion, si ocurrio lo reintenta tres veces
        while cantidad_intentos < 3:
            for respuesta in cliente.ConvertirCancionAMp3(self.enviar_cancion()):
                self.recibir_cancion(respuesta)
                if self.error is not None:
                    print("Error ocurrido:" + self.error.error)
                    cantidad_intentos += 1
                    break
            if self.error is None:
                if len(self.cancion_calidad_baja) > 0 and len(self.cancion_calidad_media) > 0 \
                        and len(self.cancion_calidad_alta) > 0:
                    if self._validar_sha256_de_canciones_recibidas():
                        print("Sha 256 valido")
                        break
                    else:
                        cantidad_intentos += 1
                else:
                    cantidad_intentos += 1
            self.error = None
