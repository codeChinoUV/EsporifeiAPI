# config/testing.py
from .default import *

# Parámetros para activar el modo debug
TESTING = True
DEBUG = True
APP_ENV = APP_ENV_TESTING
SQLALCHEMY_DATABASE_URI = "postgresql://espotifeiapi:123456@localhost:5432/espotifeitest"
