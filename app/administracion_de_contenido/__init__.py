from flask import Blueprint
from flask_restful import Api

administracion_de_contenido = Blueprint('administracion_de_contenido', __name__)
api = Api(administracion_de_contenido)

from . import EndPoints
