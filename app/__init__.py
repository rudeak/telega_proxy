from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views
from app import forms
from app import models
