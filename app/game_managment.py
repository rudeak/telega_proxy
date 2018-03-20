import requests
from app.models import Game, ArchiveGame, Chat, Chat_opt, Proxy, Gamers
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app import db
from app.gamers_managment import return_gamer_name
from app.telega_managment import return_chat_name


def new_game(domain, id, name, gamer, chat, owner):
    new_game = Game(domain, id, name, gamer, chat, owner)
    db.session.add(new_game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        print('Помилка запису параметрів гри у базу')
        return 'Помилка запису параметрів гри у базу'


def active_games_list(owner=0):
    if owner == 0:
        games = Game.query.all()
    else:
        games = Game.query.filter_by(owner=owner).all()
    game_table = []
    for game in games:
        print (Proxy.query.all())
        if  Proxy.query.filter_by (game = game.id).count()>0:
            proxies = Proxy.query.filter_by (game = game.id).all()
            for proxy in proxies:
                t = {'id': game.id, 'game_domain': game.game_domain, 'game_id': game.game_id, 'game_name': game.game_name, 'gamer': game.gamer, 'login': return_gamer_name(
                    game.gamer), 'chat': game.chat, 'chat_name': return_chat_name(game.chat)['chat_name'], 'tg_id': return_chat_name(game.chat)['chat_tg_id'],'proxy_id':proxy.key}
                game_table.append(t)
        else:
                t = {'id': game.id, 'game_domain': game.game_domain, 'game_id': game.game_id, 'game_name': game.game_name, 'gamer': game.gamer, 'login': return_gamer_name(
                    game.gamer), 'chat': game.chat, 'chat_name': return_chat_name(game.chat)['chat_name'], 'tg_id': return_chat_name(game.chat)['chat_tg_id'],'proxy_id':'None'}
                game_table.append(t)
    return game_table


def delete_game(id):
    game = Game.query.filter_by(id=id).first()
    db.session.delete(game)
    proxies = Proxy.query.filter_by (game = id).all()
    for proxy in proxies:
        db.session.delete(proxy)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollbac()
        return 'помилка видалення гри'


def archive_game(id):
    game = Game.query.filter_by(id=id).first()
    aGame = ArchiveGame()
    aGame.game_date = game.game_date
    aGame.game_domain = game.game_domain
    aGame.game_id = game.game_id
    aGame.owner = game.owner
    aGame.achive_date = datetime.now()
    db.session.add(aGame)
    db.session.delete(game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'помилка архівування гри'


def proxy_db(id):
    game = Game.query.filter_by(game_id=id).first()
    print ('proxy_db')
    print (game)
    chat = Chat.query.filter_by(id=game.chat).first()
    chat_opt = Chat_opt.query.filter_by(chat=chat.tg_id).first()
    if chat_opt.proxy:
        if chat_opt.multi_proxy:
            proxy = Proxy(game.id, chat.id)
            db.session.add(proxy)
        else:
            if Proxy.query.filter_by(game=id).count() == 0:
                proxy = Proxy(game.id, chat.id)
                db.session.add(proxy)
            else:
                proxy = Proxy.query.filter_by(game=id).first()
                proxy.game = game.id
                proxy.chat = chat.id
    try:
        db.session.commit()
        return proxy.key
    except:
        db.session.rollback()
        return 'помилка запису параметрів проксі в базу данних'

def edit_game_name (id, name):
    game = Game.query.filter_by (game_id = id).first()
    game.game_name = name
    print ('new game name ='+ name)
    try:
        print (game.game_name)
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'помилка редагування назви гри'

def get_domain (id):
    
    proxy = Proxy.query.filter_by (key = id).first()
    game = Game.query.filter_by (id = proxy.game).first()
    return game.game_domain

def get_game_id (id):
    proxy = Proxy.query.filter_by (key = id).first()
    game = Game.query.filter_by (id = proxy.game).first()
    return str(game.game_id)

def login_game (proxy_id):
    proxy = Proxy.query.filter_by (key = proxy_id).first()
    game = Game.query.filter_by (id = proxy.game).first()
    login = Gamers.query.filter_by (id = game.gamer).first().login
    password = Gamers.query.filter_by (id = game.gamer).first().password
    domain = get_domain (proxy_id)
    id = game.game_id
    r = requests.Session()
    app.game_session.append ({'game':id,'proxy':proxy,'session':r})
    page = r.get('http://'+domain+'/GameDetails.aspx?gid='+str(id))
    edit_game_name (id,  get_game_info (page))
    login_page = r.get ('http://'+domain+'/Login.aspx?login='+login+'&password='+password)
    return 1
    

