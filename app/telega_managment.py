import hashlib
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import Telegram_Users, Chat, Chat_opt

def telega_list (owner_id):
    tg_users = Telegram_Users.query.all()
    print (list(tg_users)) #list tg users
    return tg_users

def chat_list ():
    chat = Chat.query.all()
    return chat

def create_chat (tg_id, name, avatar):
    if Chat.query.filter_by (tg_id = tg_id).count() > 0:
        print ('чат з таким id існує')
        return 'чат з таким id існує'
    chat = Chat (tg_id, name, avatar, 89999)
    chat_opt = Chat_opt (tg_id)
    db.session.add (chat)
    db.session.add (chat_opt)
    try:
        db.session.commit()
        print ('чат додано')
        return 1
    except:
        db.session.rollback()
        print ('помилка при звернення до бази данних при створенні чату')
        return 'помилка при звернення до бази данних при створенні чату'

def edit_chat_options (tg_id, proxy, multi_proxy, bonuses, bonuses_count, codes, codes_deny, vote, vote_percent):
    chat_opt = Chat_opt.query.filter_by (chat = tg_id).first()
    chat_opt.proxy = proxy
    chat_opt.multi_proxy = multi_proxy
    chat_opt.bonuses = bonuses
    chat_opt.bonuses_count = bonuses_count
    chat_opt.codes = codes
    chat_opt.codes_deny = codes_deny
    chat_opt.vote = vote
    chat_opt.vote_percent = vote_percent
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'помилка при редагуванні налаштуваннь чату '+tg_id
        
def delete_chat (tg_id):
    chat = Chat.query.filter_by (tg_id = tg_id).first()
    chat_opt = Chat_opt.query.filter_by (chat = tg_id).first()
    db.session.delete (chat)
    db.session.delete (chat_opt)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'помилка при вилученні чату '+ tg_id

def return_chat_name (id):
    chat = Chat.query.filter_by(id=id).first()
    chat_dict = ['chat_name':chat.name,'chat_tg_id':chat.tg_id]
    return chat_dict
"""
def add_gamer_db(login1, password1, comment1, owner_id):
    new_gamer = Gamers (login1, password1, comment1, owner_id)
    db.session.add(new_gamer)
    db.session.commit()
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'Помилка звернення до бази даних'
"""