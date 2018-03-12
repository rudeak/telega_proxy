from app.models import Game, ArchiveGame, Chat, Proxy, User, Telegram_Users
from sqlalchemy.orm import sessionmaker
from app import db


def stats ():
    users = 0
    for user in User.query.all():
        users +=1
    games_active = 0
    for game in Game.query.all():
        games_active+=1
    games_played = 0
    #for played in ArchiveGame.query.all():
    #    games_played +=1
    active_proxy = 0
    for proxy in Proxy.query.all():
        active_proxy +=1
    return {'users':users, 
            'games_active':games_active,
            'games_played':games_played,
            'active_proxy':active_proxy}