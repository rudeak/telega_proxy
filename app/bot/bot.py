from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, current_user, login_required
import app
import telepot

bot = Blueprint('bot', 'bot', template_folder='templates')

telegram_api_key = '598589123:AAH3gPKY_4kvA50wrXQdnq6pGMd14TQId0E'

telega_bot = telepot.Bot(telegram_api_key)
telega_bot.setWebhook ('https://rudeak.gq/bot/{}'.format(telegram_api_key))

@bot.route('/'+telegram_api_key, methods = ['POST', 'GET'])
def message_listener():
    update = request.get_json()
    print (update)
    return 'bot ok'
