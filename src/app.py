from flask import Flask

from src.administracion_de_contenido.controlador.CreadoresDeContenidoControlador import CreadoresDeContenidoControlador
from src.manejo_de_usuarios.controlador.UsuariosControlador import UsuariosControlador

app = Flask(__name__)

CreadoresDeContenidoControlador.exponer_end_point(app)
UsuariosControlador.exponer_end_point(app)



if __name__ == '__main__':
    app.run(debug=True)
