from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, current_user, login_required
import app


proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
@login_required
def show():
    return render_template ('index.html', user = current_user)

@proxy.route('/proxy_creator/<id>', methods =['get'])
@login_required
def proxy_creator (id):
    return 'proxy id='+str(id)
