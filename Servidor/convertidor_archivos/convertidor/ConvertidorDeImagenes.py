import pathlib

from PIL import Image


class ConvertidorDeImagenes:
    CALIDAD_ALTA_AlTO = 600
    CALIDAD_ALTA_ANCHO = 600
    CALIDAD_MEDIA_ALTO = 300
    CALIDAD_MEDIA_ANCHO = 300
    CALIDAD_BAJA_ALTO = 150
    CALIDAD_BAJA_ANCHO = 150
    FORMATO_PNG = "png"

    def __init__(self, logger):
        self.logger = logger
        self.ubicacion_archivo = ""
        self.id_portada = 0
        self.fomato = ""
        self.ubicacion_fichero_calidad_alta = ""
        self.ubicacion_fichero_calidad_media = ""
        self.ubicacion_fichero_calidad_baja = ""

    def convertir_a_calidad_alta(self):
        """
        Convierte la portada original a png a 600*600
        :return: El lugar en donde se guardo el archivo
        """
        self.logger.info("Se empezo a convertir la portada con el id " + str(self.id_portada) + " a png calidad alta")
        self.ubicacion_fichero_calidad_alta = self._convertir_imagen(ConvertidorDeImagenes.CALIDAD_ALTA_AlTO,
                                                                     ConvertidorDeImagenes.CALIDAD_ALTA_ANCHO)
        self.logger.info("Se convirtio la portada con el id " + str(self.id_portada) + " a png en calidad alta")
        return self.ubicacion_fichero_calidad_alta

    def convertir_a_calidad_media(self):
        """
        Convierte la portada original a png a 300*300
        :return: El lugar en donde se guardo el archivo
        """
        self.logger.info("Se empezo a convertir la portada con el id " + str(self.id_portada) + " a png calidad media")
        self.ubicacion_fichero_calidad_media = self._convertir_imagen(ConvertidorDeImagenes.CALIDAD_MEDIA_ALTO,
                                                                      ConvertidorDeImagenes.CALIDAD_MEDIA_ANCHO)
        self.logger.info("Se convirtio la portada con el id " + str(self.id_portada) + " a png en calidad media")
        return self.ubicacion_fichero_calidad_media

    def convertir_a_calidad_baja(self):
        """
        Convierte la portada original a png a 300*300
        :return: El lugar en donde se guardo el archivo
        """
        self.logger.info("Se empezo a convertir la portada con el id " + str(self.id_portada) + " a png calidad baja")
        self.ubicacion_fichero_calidad_baja = self._convertir_imagen(ConvertidorDeImagenes.CALIDAD_BAJA_ALTO,
                                                                     ConvertidorDeImagenes.CALIDAD_BAJA_ANCHO)
        self.logger.info("Se convirtio la portada con el id " + str(self.id_portada) + " a png en calidad baja")
        return self.ubicacion_fichero_calidad_baja

    def _convertir_imagen(self, calidad_alto, calidad_ancho):
        try:
            imagen = Image.open(self.ubicacion_archivo)
            ruta_imagen = str(self.id_portada) + str(calidad_alto) + "x" + str(calidad_ancho) + "." + \
                          ConvertidorDeImagenes.FORMATO_PNG
            nueva_imagen = imagen.resize((calidad_alto, calidad_ancho))
            nueva_imagen.save(ruta_imagen, ConvertidorDeImagenes.FORMATO_PNG)
            return ruta_imagen
        except Exception as ex:
            self.logger.info("excepcion: " + str(ex))

    def escribir_fichero(self, id_portada, extension, arreglo_de_bytes):
        """
        Escribe en un archivo el arreglo de bytes para poder llevar a cabo su transformacion
        :param id_portada: El id que tiene la portada en la base de datos
        :param extension: La extension original del archivo
        :param arreglo_de_bytes: Los bytes que contiene el archivo
        :return: La ubicacion en donde se guardo el achivo
        """
        self.id_portada = int(id_portada)
        self.ubicacion_fichero = '/tmp/' + str(id_portada) + 'p.' + extension
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