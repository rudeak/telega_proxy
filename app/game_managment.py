from app.models import Game
from sqlalchemy.orm import sessionmaker
from app import db
from app.gamers_managment import return_gamer_name
from app.telega_managment import return_chat_name

def new_game (domain, id, name, gamer, chat, owner):
    new_game = Game (domain, id, name, gamer, chat, owner)
    db.session.add (new_game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        print ('Помилка запису параметрів гри у базу')
        return 'Помилка запису параметрів гри у базу'

def active_games_list (owner = 0):
    if owner ==0 :
        games = Game.query.all()
    else:
        games = Game.query.filter_by(owner = owner).all()
    game_table = []
    for game in games:
        t = {'game_domain':game.game_domain, 'game_id':game.game_id,'game_name':game.game_name,'gamer':game.gamer,'login':return_gamer_name(game.gamer),'chat':game.chat,'chat_name':return_chat_name (game.chat).chat_name, 'tg_id':return_chat_name (game.chat).chat_tg_id}
        game_table.append (t)
    return game_table

def delete_game (id):
    game = Game.query.filter_by (id=id).first()
    db.session.delete(game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollbac()
        return 'помилка видалення гри'
