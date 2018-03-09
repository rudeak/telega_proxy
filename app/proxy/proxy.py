from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_login import current_user
import app


proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
def show():
    return 'hello'
    
