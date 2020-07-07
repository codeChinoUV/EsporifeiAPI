from . import api
from .controlador.v1.LoginControlador import LoginControlador
from .controlador.v1.UsuarioControlador import UsuarioControlador

api.add_resource(LoginControlador, '/v1/login')
api.add_resource(UsuarioControlador, '/v1/usuario')