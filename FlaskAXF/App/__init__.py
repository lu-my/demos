from flask import Flask
from App.ext import init_ext
from App.middleware import init_middleware
from App.settings import envs
from App.views import init_views


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(envs.get(env))
    init_views(app)
    init_ext(app)
    init_middleware(app)
    return app
