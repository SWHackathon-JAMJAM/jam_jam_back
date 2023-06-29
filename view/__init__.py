from flask import Flask
from . import web
from . import honey_game
from . import menu
from . import jam_game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'

app.register_blueprint(menu.menu)
app.register_blueprint(web.web)
app.register_blueprint(honey_game.honey_game)
app.register_blueprint(jam_game.jam_game)