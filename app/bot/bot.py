from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound

import app
import telepot
from app import db
from app.models import Chat, botSignall

bot = Blueprint('bot', 'bot', template_folder='templates')

telegram_api_key = '598589123:AAH3gPKY_4kvA50wrXQdnq6pGMd14TQId0E'

telega_bot = telepot.Bot(telegram_api_key)
telega_bot.setWebhook('https://rudeak.gq/bot/{}'.format(telegram_api_key))


@bot.route('/'+telegram_api_key, methods=['POST', 'GET'])
def message_listener():
    update = request.get_json() #TODO перевірку чи такий чат є в базі якщо немає то створити
    print(update)
    return 'bot ok'

def find_chat (jsonIn):
    chat = jsonIn['chat']
    if Chat.query.filter_by(tg_id = chat['id']).count() ==0:
        if chat['id']<0:
            chat_db = Chat(chat['id'], chat['title'], "<img></img>",0)
        else:
            message = jsonIn['message']
            user = message['from']
            privat_title = 'Private chat with {}'.format(user['username'])
            chat_db = Chat(chat['id'], chat['title'], "<img></img>",0) 
    db.session.add(chat_db)
    try:
        db.session.commit()
        print ('new chat added')
    except:
        db.session.rollback()
        print ('error while adding chat to db')
    
    return None
