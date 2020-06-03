from flask import Blueprint
from flask_restful import Api

manejo_de_usuarios = Blueprint('manejo_de_usuarios', __name__)
api = Api(manejo_de_usuarios)

from . import EndPoints
