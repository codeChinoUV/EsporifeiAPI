from functools import wraps

import jwt
import datetime
from flask import request, jsonify
from flask_restful import Resource, Api

from src import app
from src.manejo_de_usuarios.modelo.enum.enums import TipoUsuario
from src.manejo_de_usuarios.modelo.modelos import Usuario


def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            error = {'error': 'token_faltante',
                     'mensaje': 'La cabecera http no lleva el token en el campo \'x-access-token\''}
            return 401, error
        try:
            datos = jwt.decode(token, app.config['SECRET_KEY'])
            usuario_actual = Usuario.obtener_usuario(datos['nombre_usuario'])
        except:
            error = {'error': 'token_invalido',
                     'mensaje': 'El token no es valido, ya sea por que se modifico o el tiempo de vida expiro'}
            return error, 401
        return f(*args, usuario_actual, **kwargs)

    return decorated


def solo_creador_de_contenido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario_actual =args[1]
        if TipoUsuario(usuario_actual.tipo_usuario) != TipoUsuario.CreadorDeContenido:
            error = {'error': 'operacion_no_permitida',
                     'mensaje': 'El usuario con el que se encuentra autenticado no tiene permisos para realizar dicha '
                                'operación'}
            return error, 403
        return f(*args, **kwargs)

    return decorador


class LoginControlador(Resource):
    api = Api()

    def get(self):
        """
        Se encarga de generar un token para autenticar a un usuario
        :return: Un token de autenticacion o un diccionario con el error y mensaje del error si ocurrio uni
        """
        login = request.authorization
        error = {'error': 'parametros_faltantes', 'mensaje': 'Los siguientes parametros faltan en tu solicitud: '}
        if not login.username and not login.password:
            error['mensaje'] += '<username>, <password>'
            return error, 400
        elif not login.username:
            error['mensaje'] += '<username>'
            return error, 400
        elif not login.password:
            error['mensaje'] += '<password>'
            return error, 400

        usuario = Usuario.validar_credenciales(login.username, login.password)
        if usuario is None:
            error = {'error': 'credenciales_invalidas', 'mensaje': 'No existe un usuario con la combinación de usuario '
                                                                   'y contrasena indicada'}
            return error, 400
        token = jwt.encode({'nombre_usuario': usuario.nombre_usuario,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    @staticmethod
    def exponer_endpoint(app):
        """
        Se encarga de exponer el endpoint de la clase en la app
        :param app: La app en donde se expondra el endpoint
        :return: None
        """
        LoginControlador.api.add_resource(LoginControlador, '/v1/login')
        LoginControlador.api.init_app(app)
