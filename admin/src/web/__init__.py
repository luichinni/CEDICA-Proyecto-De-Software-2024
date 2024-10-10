from flask import Flask
from flask import render_template
from web.handlers import error
from src.core import database
from src.core.config import config
from src.core.models import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Enviar')
    opciones = SelectField('Selecciona una opción', choices=[
            ('opcion1', 'Opción 1'),
            ('opcion2', 'Opción 2'),
            ('opcion3', 'Opción 3')
        ])
def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/prueba")
    def prueba():
        return render_template('form.html', form=MyForm() )
    
    @app.route("/pruebados")
    def pruebados():
        opciones= [
            {"value":"opcion 1",
             "text":"opcion 1"},
             {"value":"opcion 2",
             "text":"opcion 2"},
        ]
        return render_template('search_box.html', opciones_tipo = opciones, opciones = opciones)

    app.register_error_handler(404, error.not_found_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
    return app