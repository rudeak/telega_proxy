from app.models import Game
from sqlalchemy.orm import sessionmaker
from app import db

def new_game (domain, id, name, gamer, chat):
    new_game = Game (domain, id, name, gamer, chat)
    db.session.add (new_game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        print ('Помилка запису параметрів гри у базу')
        return 'Помилка запису параметрів гри у базу'

def active_games_list ():
    return Game.query.all()

def delete_game (id):
    game = Game.query.filter_by (id=id).first()
    db.session.delete(game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollbac()
        return 'помилка видалення гри'
