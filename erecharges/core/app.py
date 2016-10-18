# -*- coding: utf-8 -*-
from erecharges.blueprints.home.views import bp_home
from flask import Flask


def create_app():
    app = Flask('erecharges', instance_relative_config=True)
    _load_config(app)
    _setup_db(app)
    _setup_extensions(app)
    _register_blueprints(app)
    return app

def _load_config(app):
    app.config.from_object('erecharges.settings')
    app.config.from_pyfile('settings.py')

def _setup_db(app):
    pass

def _setup_extensions(app):
    pass

def _register_blueprints(app):
    app.register_blueprint(bp_home)