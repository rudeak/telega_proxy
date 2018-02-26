import hashlib
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import Telegram_Users

def telega_list (owner_id):
    tg_users = Telegram_Users.query.filter_by(creator_id = owner_id)
    print (tg_users)
    return tg_users


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