from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src import Configuracion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Configuracion.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Configuracion.SQL_ALCHEMY_TRACK_MODIFICATIONS
base_de_datos = SQLAlchemy(app)