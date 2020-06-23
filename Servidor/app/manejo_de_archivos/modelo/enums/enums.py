from enum import Enum

class FormatoAudio(Enum):
    MP3 = "mp3"
    M4A = "m4a"
    FLAC = "flac"

class Calidad(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3

class FormatoImagen(Enum):
    PNG = "png"
    JPG = "jpg"
