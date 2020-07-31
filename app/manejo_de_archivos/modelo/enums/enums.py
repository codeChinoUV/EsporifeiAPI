from enum import Enum

class FormatoAudio(Enum):
    MP3 = "mp3"
    M4A = "m4a"
    FLAC = "flac"
    WAV = "wav"

class Calidad(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3
    ORIGINAL = 4

class FormatoImagen(Enum):
    PNG = "png"
    JPG = "jpg"
