import json
from app import db
from app.models import EnGame, EnLvl
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.game_managment import edit_game_name, get_domain, get_game_id


def en_game_info_create(page, user_id):
    return 1

def en_game_logger (proxy_key, page_json):
    print (page_json)
    #print ('game id ='+str(get_game_id(proxy_key)))
    # створення нової гри
    if EnGame.query.filter_by (en_game_id = get_game_id(proxy_key), proxy_key = proxy_key).count()==0:
        print ('new game found')
        game = EnGame (get_game_id(proxy_key), proxy_key)
        db.session.add (game)
        try:
            db.session.commit()
        except:
            print ('помилка створення нового сценарю гри')
            db.session.rollback()
    # створення нового рівня
    levelInfo = json.loads(page_json ['levelinfo'])
    #print (levelInfo['levelId'])
    if EnLvl.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).count() == 0:
        lvl = EnLvl (get_game_id(proxy_key), levelInfo['levelId'], levelInfo['levelNum'])
        db.session.add(lvl)
        #print ('new level found')
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print('помилка створення новго рівня гри')

    return 1

def en_level_info_updater (lvl):
    return None

