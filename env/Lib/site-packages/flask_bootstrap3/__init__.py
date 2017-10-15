# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, url_for

class Bootstrap(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint(
            'bootstrap',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/bootstrap'
        )

        app.register_blueprint(blueprint)

