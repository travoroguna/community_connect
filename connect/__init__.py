import flask
import toml
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



def create_app(config=None) -> flask.Flask:
    app = flask.Flask(__name__, isinstance_relative_config=True)

    if config is None:
        app.config_from_file("config_dev.toml", silent=True)
    else:
        app.config_from_file(config, load=toml.load, silent=True)

    with app.app_context():
        create_services(app)

    return app


def create_services(app: flask.Flask):
    #setup database and migrations
    db = SQLAlchemy(app)
    Migrate(app, db)

    #create tables
    db.create_all()
    db.session.commit()

    


