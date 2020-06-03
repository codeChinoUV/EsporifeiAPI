from flask_restful import Resource, reqparse, Api

from app.administracion_de_contenido.modelo.modelos import Disquera
from app.manejo_de_usuarios.controlador.v1.LoginControlador import solo_creador_de_contenido, token_requerido
from app.util.validaciones.modelos.ValidacionDisquera import ValidacionDisquera


class DisquerasControlador(Resource):
    api = Api()

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nombre')
        self.parser.add_argument('direccion')
        self.parser.add_argument('email')
        self.parser.add_argument('telefono')
        self.parser.add_argument('es_empresa')
        self.argumentos = self.parser.parse_args(strict=True)

    @token_requerido
    @solo_creador_de_contenido
    def post(self, usuario_actual):
        """
        Se encarga de registrar una nueva disquera
        :return: Una lista de errores de los errores en la solictud o un diccionario con los datos de la disquera
         registrada
        """
        disquera = Disquera(nombre=self.argumentos['nombre'], direccion=self.argumentos['direccion'],
                            email=self.argumentos['email'], telefono=self.argumentos['telefono'],
                            es_empresa=self.argumentos['es_empresa'],
                            nombre_usuario_creador=usuario_actual.nombre_usuario)
        errores_de_validacion = ValidacionDisquera.validar_registro_disquera(disquera)
        if len(errores_de_validacion) > 0:
            return errores_de_validacion, 400
        disquera.guardar()
        return disquera.obtner_json(), 201

    @staticmethod
    def exponer_end_point(app):
        """
        Expone los metodos del endpoint
        :param app: La aplicacion en la cual se expondra el endpoint
        """
        DisquerasControlador.api.add_resource(DisquerasControlador,
                                              '/v1/disqueras')

        DisquerasControlador.api.init_app(app)
