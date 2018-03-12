from datetime import datetime
from hashlib import md5
from random import randint
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_SUPERUSER = 2

TELEGA_USER = 0
TELEGA_ADMIN = 1
TELEGA_SUPERUSER = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120), index = True, unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__ (self, login, email, password , role):
        self.login = login
        self.email = email
        self.password = password
        self.role = role
        

    def __repr__(self):
        return '<User %r>' % (self.login)
        
    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode()).hexdigest() + '?d=mm&s=' + str(size)


class Gamers (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = False)
    password = db.Column(db.String(120), index = True, unique = False)
    comment = db.Column(db.String(120), index = True, unique = False)
    creator_id = db.Column(db.Integer)    
    
    def __repr__(self):
        return '<User %r>' % (self.login)

    def __init__ (self, login, password , comment,  creator_id):
        self.login = login
        self.password = password
        self.comment = comment
        self.creator_id = creator_id

class Telegram_Users (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tg_login = db.Column(db.String(64), index = True, unique = True)
    tg_id = db.Column(db.String(64), index = True, unique = True)
    telega_id = db.Column(db.Integer,index = True, unique = False)
    telega_role = db.Column(db.SmallInteger, default = TELEGA_USER)
    creator_id = db.Column(db.Integer)    
    
    def __repr__(self):
        return '<User %r>' % (self.tg_login)

    def __init__ (self, tg_login, tg_id , telega_id,  telega_role, creator_id):
        self.tg_login = tg_login
        self.tg_id = tg_id
        self.telega_id = telega_id
        self.telega_role = telega_role
        self.creator_id = creator_id

class Chat (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tg_id = db.Column(db.Integer, index = True, unique = True)
    name = db.Column(db.String(120), index = True, unique = False)
    avatar = db.Column(db.String(120), index = True, unique = False)
    game_id = db.Column(db.Integer)
    chat_date = db.Column (db.DateTime)

    
    def __repr__(self):
        return '<Chat %r>' % (self.name)

    def __init__ (self, tg_id, name , avatar,  game_id):
        self.tg_id = tg_id
        self.name = name
        self.avatar = avatar
        self.game_id = game_id
        self.chat_date = datetime.now()

class Chat_opt (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chat = db.Column(db.Integer, unique = True)
    proxy = db.Column (db.Boolean, default = True)
    multi_proxy = db.Column (db.Boolean, default = False)
    bonuses = db.Column (db.Boolean, default = True)
    bonuses_count = db.Column (db.Integer, default = 5)
    codes =  db.Column (db.Boolean, default = True)
    codes_deny = db.Column (db.Boolean, default = True)
    vote = db.Column (db.Boolean, default = True)
    vote_percent = db.Column (db.Integer, default = 30)

    def __repr__(self):
        return '<Chat %r>' % (self.chat)

    def __init__ (self, chat):
        self.chat = chat
        self.proxy = True
        self.multi_proxy = False
        self.bonuses = True
        self.bonuses_count = 5
        self.codes = True 
        self.codes_deny = True
        self.vote = True
        self.vote_percent = 30

class Game (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    game_date = db.Column (db.DateTime)
    game_domain = db.Column(db.String(120))
    game_id = db.Column(db.Integer)
    game_name = db.Column(db.String(120), index = True, unique = False)
    gamer = db.Column(db.Integer)
    chat = db.Column(db.Integer)
    owner = db.Column(db.Integer)

    def __repr__(self):
        return '<Game %r>' % (self.game_name)
    
    def __init__(self, game_domain, game_id, game_name, gamer, chat, owner):
        self.game_id = game_id
        self.game_domain = game_domain
        self.game_name = game_name
        self.gamer = gamer
        self.chat = chat
        self.game_date = datetime.now()
        self.owner = owner

class ArchiveGame (Game):
#    id = db.Column(db.Integer, primary_key = True)
    achive_date = db.Column (db.DateTime)

    def __repr__(self):
        return '<Game %r>' % (self.game_name)
    
    def __init__ (self, achive_date):
        self.achive_date = datetime.now()

class Proxy (Model):
    game = db.Column(db.Integer)
    chat = db.Column(db.Integer)
    key = db.Column(db.Integer)
    creation_date = db.Column (db.DateTime)

    def __repr__(self):
        return '<Game proxy %r>' % (self.game)

    def __init__ (self, game, chat):
        self.game = game
        self.chat = chat
        self.creation_date = datetime.now()
        key = randint (1000000, 9999999)
        while Proxy.query.filter_by (key = key).count !=0:
            key = randint (1000000, 9999999)
        self.key = key
