
from src import app
from src.administracion_de_contenido.controlador.CreadoresDeContenidoControlador import CreadoresDeContenidoControlador
from src.manejo_de_usuarios.controlador.UsuariosControlador import UsuariosControlador


CreadoresDeContenidoControlador.exponer_end_point(app)
UsuariosControlador.exponer_end_point(app)

if __name__ == '__main__':
    app.run(debug=True)
