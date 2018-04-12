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
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __init__(self, login, email, password, role):
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
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=False)
    password = db.Column(db.String(120), index=True, unique=False)
    comment = db.Column(db.String(120), index=True, unique=False)
    creator_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % (self.login)

    def __init__(self, login, password, comment,  creator_id):
        self.login = login
        self.password = password
        self.comment = comment
        self.creator_id = creator_id


class Telegram_Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tg_login = db.Column(db.String(64), index=True, unique=True)
    tg_id = db.Column(db.String(64), index=True, unique=True)
    telega_id = db.Column(db.Integer, index=True, unique=False)
    telega_role = db.Column(db.SmallInteger, default=TELEGA_USER)
    creator_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % (self.tg_login)

    def __init__(self, tg_login, tg_id, telega_id,  telega_role, creator_id):
        self.tg_login = tg_login
        self.tg_id = tg_id
        self.telega_id = telega_id
        self.telega_role = telega_role
        self.creator_id = creator_id


class Chat (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(120), index=True, unique=False)
    avatar = db.Column(db.String(120), index=True, unique=False)
    game_id = db.Column(db.Integer)
    chat_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Chat %r>' % (self.name)

    def __init__(self, tg_id, name, avatar,  game_id):
        self.tg_id = tg_id
        self.name = name
        self.avatar = avatar
        self.game_id = game_id
        self.chat_date = datetime.now()


class Chat_opt (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.Integer, unique=True)
    proxy = db.Column(db.Boolean, default=True)
    multi_proxy = db.Column(db.Boolean, default=False)
    bonuses = db.Column(db.Boolean, default=True)
    bonuses_count = db.Column(db.Integer, default=5)
    codes = db.Column(db.Boolean, default=True)
    codes_deny = db.Column(db.Boolean, default=True)
    vote = db.Column(db.Boolean, default=True)
    vote_percent = db.Column(db.Integer, default=30)

    def __repr__(self):
        return '<Chat %r>' % (self.chat)

    def __init__(self, chat):
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
    id = db.Column(db.Integer, primary_key=True)
    game_date = db.Column(db.DateTime)
    game_domain = db.Column(db.String(120))
    game_id = db.Column(db.Integer)
    game_name = db.Column(db.String(120), index=True, unique=False)
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
    achive_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Game %r>' % (self.game_name)

    def __init__(self, achive_date):
        self.achive_date = datetime.now()


class Proxy (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer)
    chat = db.Column(db.Integer)
    key = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Game proxy %r>' % (self.game)

    def __init__(self, game, chat):
        self.game = game
        self.chat = chat
        self.creation_date = datetime.now()
        key = randint(1000000, 9999999)
        while Proxy.query.filter_by(key=key).count() != 0:
            print ('key ='+str(key))
            key = randint(1000000, 9999999)
        self.key = key
    
class GameInfo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    game_name = db.Column(db.String(120), index=True, unique=False)
    game_description = db.Column (db.Text)
    game_start = db.Column (db.DateTime)
    game_owner = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Game name %r>' % (self.game_name)
    
    def __init__(self, game_id, game_name, game_description,game_start, game_owner):
        self.game_id = game_id
        self.game_name = game_name
        self.game_description = game_description
        self.game_start = game_start
        self.game_owner = game_owner
        
#--------------------------------
# моделі сценарія гри
#--------------------------------

class EnGameJson( db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    json = db.Column (db.Text)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnJson(%(json)s, %(id)s)>" % self.__dict__
    
    def __init__ (self, json):
        self.json = json


class EnGame(db.Model):



    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    en_game_id = db.Column(db.Integer)
    proxy_key = db.Column(db.Integer)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnGame(%(en_game_id)s, %(id)s)>" % self.__dict__
    
    def __init__(self, en_game_id, proxy_key):
        self.en_game_id = en_game_id
        self.proxy_key = proxy_key


class EnLvl(db.Model):



    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    en_game_id = db.Column(db.Integer)
    en_lvl_id = db.Column(db.Integer)
    en_lvl_no = db.Column(db.Integer)
    en_answer_block = db.Column(db.Boolean)
    en_sectors_count = db.Column(db.Integer)
    en_sectors_need = db.Column(db.Integer)
    en_sectors_closed = db.Column(db.Integer)
    

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnLvl(%(id)s, %(en_lvl_no)s)>" % self.__dict__

    def __init__(self, en_game_id, en_lvl_id, en_lvl_no):
        self.en_game_id = en_game_id
        self.en_lvl_id = en_lvl_id
        self.en_lvl_no = en_lvl_no

class EnSectors (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    en_game_id = db.Column(db.Integer)
    en_lvl_id = db.Column(db.Integer)
    en_lvl_no = db.Column(db.Integer)
    en_sector_no = db.Column(db.Integer)
    en_sector_name = db.Column(db.Text)
    en_sector_entered = db.Column(db.Boolean)
    en_sector_answer = db.Column(db.Text)
    en_gamer = db.Column(db.Text)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnSectors(%(id)s, %(en_sector_name)s)>" % self.__dict__
    
    def __init__(self, en_game_id, en_lvl_id, en_lvl_no, en_sector_no, en_sector_name, en_sector_entered, en_sector_answer, en_gamer):
        self.en_game_id = en_game_id
        self.en_lvl_id = en_lvl_id
        self.en_lvl_no = en_lvl_no
        self.en_sector_no = en_sector_no
        self.en_sector_name = en_sector_name
        self.en_sector_entered = en_sector_entered
        self.en_sector_answer = en_sector_answer
        self.en_gamer = en_gamer

class EnTask (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    en_game_id = db.Column(db.Integer)
    en_lvl_id = db.Column(db.Integer)
    en_lvl_no = db.Column(db.Integer)
    en_task_text = db.Column(db.Text)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnTask(%(id)s, %(en_task_text)s)>" % self.__dict__
    
    def __init__(self, en_game_id, en_lvl_id, en_lvl_no, en_task_text):
        self.en_game_id = en_game_id
        self.en_lvl_id = en_lvl_id
        self.en_lvl_no = en_lvl_no
        self.en_task_text = en_task_text

class EnPrompt (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    en_game_id = db.Column(db.Integer)
    en_lvl_id = db.Column(db.Integer)
    en_lvl_no = db.Column(db.Integer)
    en_prompt_no = db.Column(db.Integer)
    en_prompt_text = db.Column(db.Text)
    en_prompt_data = db.Column(db.Integer)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnPrompt(%(id)s, %(en_prompt_text)s)>" % self.__dict__
    
    def __init__(self, en_game_id, en_lvl_id, en_lvl_no, en_prompt_no, en_prompt_text, en_prompt_data):
        self.en_game_id = en_game_id
        self.en_lvl_id = en_lvl_id
        self.en_lvl_no = en_lvl_no
        self.en_prompt_no = en_prompt_no
        self.en_prompt_text = en_prompt_text
        self.en_prompt_data = en_prompt_data


"""
class EnTask(db.Model):



    id = db.Column(db.Integer, autoincrement=False, primary_key=True, nullable=False)  # pylint: disable=invalid-name
    en_level_id = db.Column(db.Integer)
    en_task_text = db.Column(db.Text)
   

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnTask(%(id)s)>" % self.__dict__


class EnPrompt(db.Model):



    id = db.Column(db.Integer, autoincrement=False, primary_key=True, nullable=False)  # pylint: disable=invalid-name
    en_level_id = db.Column(db.Integer)
    en_prompt_no = db.Column(db.SmallInteger)
    en_prompt_text = db.Column(db.Text)
    en_prompt_time = db.Column(db.Float)

    

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnPrompt(%(id)s)>" % self.__dict__


class EnBonus(db.Model):



    id = db.Column(db.Integer, autoincrement=False, primary_key=True, nullable=False)  # pylint: disable=invalid-name
    en_lvl_id = db.Column(db.Integer)
    en_bonus_no = db.Column(db.Integer)
    en_bonus_text = db.Column(db.Text)

    

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnBonus(%(id)s)>" % self.__dict__


class EnPenalty(db.Model):



    id = db.Column(db.Integer, autoincrement=False, primary_key=True, nullable=False)  # pylint: disable=invalid-name
    en_lvl_id = db.Column(db.Integer)
    en_penalty_no = db.Column(db.Integer)
    en_penalty_text = db.Column(db.Text)

    

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnPenalty(%(id)s)>" % self.__dict__

class EnLog(db.Model):

    id = db.Column(db.Integer, autoincrement=False, primary_key=True, nullable=False)  # pylint: disable=invalid-name
    en_lvl_id = db.Column(db.Integer)
    en_gamer = db.Column(db.String(200))
    en_answer = db.Column (db.String(200))
    en_is_answer = db.Column (db.Boolean)
    en_is_correct = db.Column (db.Boolean)
    en_date = db.Column (db.Float)
   

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<EnLog(%(id)s)>" % self.__dict__
"""