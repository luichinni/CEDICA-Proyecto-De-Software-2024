from flask import Flask
from flask import render_template
from web.handlers import error
from src.core import database
from src.core.config import config


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")


    app.register_error_handler(404, error.not_found_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
    return app