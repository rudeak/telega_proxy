from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_login import current_user
from app import game_managment


proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
def show(page):
    return 'hello'
    
