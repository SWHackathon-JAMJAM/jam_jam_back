from flask import Flask
from . import web
from . import game
from . import menu

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'

app.register_blueprint(menu.menu)
app.register_blueprint(web.web)
app.register_blueprint(game.game)