import jwt
import datetime
from flask import request, jsonify
from flask_restful import Resource, Api

from src import app
from src.manejo_de_usuarios.modelo.modelos import Usuario


class LoginControlador(Resource):
    api = Api()

    def get(self):
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
        LoginControlador.api.add_resource(LoginControlador, '/v1/login')
        LoginControlador.api.init_app(app)
