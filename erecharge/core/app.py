# -*- coding: utf-8 -*-
from erecharge.blueprints.home.views import bp_home
from flask import Flask


def create_app():
    app = Flask('erecharge', instance_relative_config=True)
    _load_config(app)
    _setup_db(app)
    _setup_extensions(app)
    _register_blueprints(app)
    return app

def _load_config(app):
    app.config.from_object('erecharge.settings')
    app.config.from_pyfile('settings.py')

def _setup_db(app):
    pass

def _setup_extensions(app):
    pass

def _register_blueprints(app):
    app.register_blueprint(bp_home)