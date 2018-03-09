import hashlib
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import Gamers

def gamers_list (owner_id):
    return Gamers.query.filter_by(creator_id = owner_id).all()

def add_gamer_db(login1, password1, comment1, owner_id):
    new_gamer = Gamers (login1, password1, comment1, owner_id)
    db.session.add(new_gamer)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'Помилка звернення до бази даних'

def return_gamer_name (id):
    if Gamers.query.filter_by(id = id).count()>0:
        gamer = Gamers.query.filter_by(id = id).first()
        return gamer.login
    else
        return 'error'
    
