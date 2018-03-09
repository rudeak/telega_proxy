from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

proxy = Blueprint('proxy', __name__,
                        template_folder='templates')

@proxy.route('/', defaults={'page': 'index'})
@proxy.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)