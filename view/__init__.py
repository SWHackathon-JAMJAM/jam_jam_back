from flask import Flask
from . import web
from . import game

app = Flask(__name__)
app.register_blueprint(web.web)
app.register_blueprint(game.game)
