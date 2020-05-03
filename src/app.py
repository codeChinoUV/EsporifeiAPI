from src import app, base_de_datos
from src.administracion_de_contenido.controlador.CreadorDeContenidoControlador import CreadorDeContenidoControlador, \
    CreadorDeContenidoUsuarioControlador
from src.administracion_de_contenido.controlador.CreadoresDeContenidoControlador import \
    CreadoresDeContenidoControlador
from src.administracion_de_contenido.controlador.v1.CreadoresDeContenidoBuscarControlador import \
    CreadoresDeContenidoBuscarControlador
from src.manejo_de_usuarios.controlador.v1.UsuariosControlador import UsuariosControlador

#Expones endpoint de usuarios
UsuariosControlador.exponer_end_point(app)

#Exponemos endpoint de creadores de contenido
CreadorDeContenidoControlador.exponer_end_point(app)
CreadoresDeContenidoControlador.exponer_end_point(app)
CreadoresDeContenidoBuscarControlador.exponer_end_point(app)

#Exponemos endpoint para usuarios de creadores de contenido
CreadorDeContenidoUsuarioControlador.exponer_end_point(app)



base_de_datos.create_all()
if __name__ == '__main__':
    app.run(debug=True)
