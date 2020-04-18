from flask import Flask
from src import Configuracion
from src.manejo_de_usuarios.controlador.UsuariosControlador import UsuariosControlador

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Configuracion.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Configuracion.SQL_ALCHEMY_TRACK_MODIFICATIONS

UsuariosControlador.exponer_endpoint(app)

if __name__ == '__main__':
    app.run(debug=True)
