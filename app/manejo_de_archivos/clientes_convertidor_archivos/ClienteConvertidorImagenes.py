import hashlib
import pathlib

import grpc
from app import ServidorManejadorDeArchivos
from app.manejo_de_archivos.protos_convertidor_de_archivos import ConvertidorDeArchivos_pb2
from app.manejo_de_archivos.protos_convertidor_de_archivos import ConvertidorDeArchivos_pb2_grpc


class ConvertidorDeImagenesCliente:
    def __init__(self, id_portada, ubicacion_archivo, extension):
        self.id_portada = id_portada
        self.extension = extension
        # Tamaño de 64 Kb
        self.tamano_chunk = 1000 * 64
        self.ubicacion_archivo = ubicacion_archivo
        self.informacion_archivo = ConvertidorDeArchivos_pb2.InformacionArchivo()
        self.imagen_calidad_alta = bytearray()
        self.informacion_archivo_calidad_alta = None
        self.imagen_calidad_media = bytearray()
        self.informacion_archivo_calidad_media = None
        self.imagen_calidad_baja = bytearray()
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

    def _validar_sha256_de_imagenes_recibidas(self):
        hash256_imagen_calidad_alta = hashlib.sha3_256(self.imagen_calidad_alta).hexdigest()
        hash256_imagen_calidad_media = hashlib.sha3_256(self.imagen_calidad_media).hexdigest()
        hash256_imagen_calidad_baja = hashlib.sha3_256(self.imagen_calidad_baja).hexdigest()
        return hash256_imagen_calidad_alta == self.informacion_archivo_calidad_alta.hash256 and \
               hash256_imagen_calidad_media == self.informacion_archivo_calidad_media.hash256 and \
               hash256_imagen_calidad_baja == self.informacion_archivo_calidad_baja.hash256

    def enviar_imagen(self):
        with open(self.ubicacion_archivo, 'rb') as archivo:
            solicitud = ConvertidorDeArchivos_pb2.SolicitudConvertirPortada()
            solicitud.informacionImagen.idElemento = self.id_portada
            solicitud.informacionImagen.extension = self.extension
            solicitud.informacionImagen.hash256 = self.informacion_archivo.hash256
            for bloque in iter(lambda: archivo.read(self.tamano_chunk), b""):
                solicitud.data = bloque
                yield solicitud

    def recibir_imagen(self, respuesta):
        if respuesta.error.error != "":
            self.error = respuesta.error
        if len(respuesta.imagenCalidadAlta.data) > 0:
            self.imagen_calidad_alta += bytearray(respuesta.imagenCalidadAlta.data)
            if respuesta.imagenCalidadAlta.informacionImagen is not None:
                self.informacion_archivo_calidad_alta = respuesta.imagenCalidadAlta.informacionImagen
        if len(respuesta.imagenCalidadMedia.data) > 0:
            self.imagen_calidad_media += bytearray(respuesta.imagenCalidadMedia.data)
            if respuesta.imagenCalidadMedia.informacionImagen is not None:
                self.informacion_archivo_calidad_media = respuesta.imagenCalidadMedia.informacionImagen
        if len(respuesta.imagenCalidadBaja.data) > 0:
            self.imagen_calidad_baja += bytearray(respuesta.imagenCalidadBaja.data)
            if respuesta.imagenCalidadBaja.informacionImagen is not None:
                self.informacion_archivo_calidad_baja = respuesta.imagenCalidadBaja.informacionImagen

    def enviar_archivo(self):
        canal = grpc.insecure_channel(ServidorManejadorDeArchivos.direccion_ip_convertidor_archivos + ':' +
                                      str(ServidorManejadorDeArchivos.puerto_convertidor_archivos))
        cliente = ConvertidorDeArchivos_pb2_grpc.ConvertidorDeImagenesStub(canal)
        existe_el_archivo = self._validar_existe_archivo()
        if existe_el_archivo is not None:
            return existe_el_archivo
        self.informacion_archivo.hash256 = self._obtener_sha256(self.ubicacion_archivo)
        cantidad_intentos = 0
        # Valida si no ocurrio un error al convertir la imagen, si ocurrio lo reintenta tres veces
        while cantidad_intentos < 3:
            for respuesta in cliente.ConvertirImagenAPng(self.enviar_imagen()):
                self.recibir_imagen(respuesta)
                if self.error is not None:
                    cantidad_intentos += 1
                    break
            if self.error is None:
                if len(self.imagen_calidad_baja) > 0 and len(self.imagen_calidad_media) > 0 \
                        and len(self.imagen_calidad_alta) > 0:
                    if self._validar_sha256_de_imagenes_recibidas():
                        break
                    else:
                        cantidad_intentos += 1
                else:
                    cantidad_intentos += 1
            self.error = None
