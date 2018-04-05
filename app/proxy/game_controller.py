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
    if page_json['levelinfo'] == False:
        return 0
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
            en_level_info_updater (proxy_key, page_json)
        except:
            db.session.rollback()
            print('помилка створення новго рівня гри')
    else:
        lvl = EnLvl.query.filter_by(en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).first()
        en_level_info_updater (proxy_key, page_json)
        print ('old level found')
        #print (lvl)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print ('Помилка оновлення даних рівня')
    return 1

def en_level_info_updater (proxy_key, pageJson):
    levelInfo = json.loads(pageJson ['levelinfo'])
    lvl = EnLvl.query.filter_by(en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).first()
    print (lvl)
    lvl.en_answer_block = pageJson['block']
    sectors_counter = json.loads(pageJson['sectors_count'])
    lvl.en_sectors_count = sectors_counter['all']
    en_sectors_need =  sectors_counter ['need']
    sectors_counter = json.loads (pageJson['sectors_info'])
    print (sectors_counter)
    closed = 0
    for sector in sectors_counter:
        if sector['entered']:
            closed +=1
    en_sectors_closed = closed
    print(lvl.en_sectors_closed)
    return None

