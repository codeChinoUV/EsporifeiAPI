"""
Archivo de configuracion para el proyecto Espotifei
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "hola como estas"

DB_CONNECTION_STRING = "postgresql://espotifeiapi:123456@localhost:5432/espotifei"

SQL_ALCHEMY_TRACK_MODIFICATIONS = False
