from app import db
from app.models import EnGame
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.game_managment import edit_game_name, get_domain, get_game_id


def en_game_info_create(page, user_id):
    return 1

def en_game_logger (proxy_key, page_json):
    #print (page_json)
    #print ('game id ='+str(get_game_id(proxy_key)))
    if EnGame.query.filter_by (en_game_id = get_game_id(proxy_key), proxy_key = proxy_key).count()==0:
        print ('new game found')
        game = EnGame (get_game_id(proxy_key), proxy_key)
        db.session.add (game)
        try:
            db.session.commit()
        except:
            print ('помилка створення нового сценарю гри')
            db.session.rollback()
    levelInfo = page_json ['levelinfo']['levelId']
    print (levelInfo)
    return 1

