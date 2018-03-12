from app.models import Game, ArchiveGame, Chat, Proxy, User, Telegram_Users
from sqlalchemy.orm import sessionmaker
from app import db


def stats ():
    return {'users':User.query.all().count(), 'games_active':Game.query.all().count(), 'games_played':ArchiveGame.query.all.count(), 'active_proxy':Proxy.query.all().count()}