from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app import lm

proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
@login_required
def show(page):
    return 'hello world'
