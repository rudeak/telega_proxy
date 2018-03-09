from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app import db, lm

proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
def show(page):
    return 'hello world'
