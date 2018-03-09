from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, current_user, login_required
import app

bot = Blueprint('bot', 'bot', template_folder='templates')

@bot.route('/')
def message_listener():
    return render_template ('index.html', user = current_user)
