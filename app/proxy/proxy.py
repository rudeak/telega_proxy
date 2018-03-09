from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/', defaults={'page': 'index'})
@proxy.route('/proxy')
def show(page):
    return 'hello world'
