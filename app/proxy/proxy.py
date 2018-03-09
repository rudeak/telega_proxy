from flask import Blueprint, render_template, abort, g
from jinja2 import TemplateNotFound
from flask_login import current_user, login_required
import app


proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
@login_required
def show():
    return g.id
    
