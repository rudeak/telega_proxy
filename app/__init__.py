from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.proxy.proxy import proxy
from app.proxy.parser import get_game_info
from app.proxy.game_controller import edit_game_name
from app.bot.bot import bot
from app.api.api import api
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object('config')
app.config['TESTING'] = False
app.register_blueprint(proxy , url_prefix='/proxy')
app.register_blueprint(bot , url_prefix='/bot')
app.register_blueprint(api , url_prefix='/api')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views
from app import forms
from app import models
