from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound

import app
import telepot
from app import db

bot = Blueprint('bot', 'bot', template_folder='templates')

telegram_api_key = '598589123:AAH3gPKY_4kvA50wrXQdnq6pGMd14TQId0E'

telega_bot = telepot.Bot(telegram_api_key)
telega_bot.setWebhook('https://rudeak.gq/bot/{}'.format(telegram_api_key))


@bot.route('/'+telegram_api_key, methods=['POST', 'GET'])
def message_listener():
    update = request.get_json()
    print(update)
    return 'bot ok'
