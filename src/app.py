from src import app, base_de_datos
from src.administracion_de_contenido.controlador.CreadorDeContenidoControlador import CreadorDeContenidoControlador
from src.administracion_de_contenido.controlador.CreadoresDeContenidoControlador import CreadoresDeContenidoControlador
from src.manejo_de_usuarios.controlador.UsuariosControlador import UsuariosControlador

CreadorDeContenidoControlador.exponer_end_point(app)
CreadoresDeContenidoControlador.exponer_end_point(app)
UsuariosControlador.exponer_end_point(app)

base_de_datos.create_all()
if __name__ == '__main__':
    app.run(debug=True)
