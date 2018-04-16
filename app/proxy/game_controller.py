import json
from app import db
from app.models import EnGame, EnLvl, EnSectors, EnTask, EnPrompt, EnBonus, EnHistory
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.game_managment import edit_game_name, get_domain, get_game_id


def en_game_info_create(page, user_id):
    return 1

def en_game_logger (proxy_key, page_json):
    print (page_json)
    if page_json['levelinfo'] == False:
        return 0
    # print ('game id ='+str(get_game_id(proxy_key)))
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
    en_lvl_id = levelInfo['levelId']
    en_lvl_no = levelInfo['levelNum']
    #print (levelInfo['levelId'])
    if EnLvl.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).count() == 0:
        lvl = EnLvl (get_game_id(proxy_key), levelInfo['levelId'], levelInfo['levelNum'])
        db.session.add(lvl)
        #print ('new level found')
        try:
            db.session.commit()
            en_level_info_updater (proxy_key, page_json)
            en_task_logger (proxy_key, levelInfo['levelId'], levelInfo['levelNum'], page_json)
            en_prompts_loger (proxy_key, en_lvl_id, en_lvl_no, page_json)
            en_bonus_logger (proxy_key, en_lvl_id, en_lvl_no, page_json)
            en_history_logger (proxy_key, en_lvl_id, en_lvl_no, page_json)
        except:
            db.session.rollback()
            print('помилка створення новго рівня гри')
    else:
 #       lvl = EnLvl.query.filter_by(en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).first()
        en_level_info_updater (proxy_key, page_json)
        en_task_logger (proxy_key, levelInfo['levelId'], levelInfo['levelNum'], page_json)
        en_prompts_loger (proxy_key, en_lvl_id, en_lvl_no, page_json)
        en_bonus_logger (proxy_key, en_lvl_id, en_lvl_no, page_json)
        en_history_logger (proxy_key, en_lvl_id, en_lvl_no, page_json)
        print ('old level found')
        #print (lvl)

    return 1

def en_level_info_updater (proxy_key, pageJson):
    levelInfo = json.loads(pageJson ['levelinfo'])
    lvl = EnLvl.query.filter_by(en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).first()
    # TODO перевірка чи нічого не змінилося в рівні і додавання в сигнали боту
    lvl.en_answer_block = pageJson['block']
    sectors_counter = json.loads(pageJson['sectors_count'])
    lvl.en_sectors_count = sectors_counter['all']
    lvl.en_sectors_need =  sectors_counter ['need']
    sectors_counter = json.loads (pageJson['sectors_info'])
    
    en_sectors_logger (proxy_key, levelInfo['levelId'], levelInfo['levelNum'], sectors_counter)
    closed = 0
    for sector in sectors_counter:
        if sector['entered']:
            closed +=1
    lvl.en_sectors_closed = closed
    try:
            db.session.commit()
    except:
            db.session.rollback()
            print ('Помилка оновлення даних рівня')
    return None

def en_sectors_logger (proxy_key, en_lvl_id, en_lvl_no, sectorsJson):
    # TODO перевірка чи не змінилась кількість секторів і їх назви і закритість
    print ('sectors' + str(sectorsJson))
    
    print ('sectors count'+ str (sectors_counter(sectorsJson)))

    print ('sectors in DB ' + str(EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = en_lvl_id, en_lvl_no = en_lvl_no).count()))

    #print_sectors_from_db (proxy_key, en_lvl_id, en_lvl_no)

    # якщо ще не внесені сектори в рівень то створюємо нові
    if EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = en_lvl_id, en_lvl_no = en_lvl_no).count() == 0:
        print ('no sectors was logged!!!') #TODO повідомлення про додавання секторів
        counter = 1
        print ('------------------------START adding sector printing -------------------')
        for sectors in sectorsJson:
            print ('sector #' + str(counter) + ' name = '+ sectors['name'])
            en_sector = EnSectors(get_game_id(proxy_key), 
                                  en_lvl_id, 
                                  en_lvl_no, 
                                  counter, 
                                  sectors['name'],
                                  sectors['entered'],
                                  sectors['answer'],
                                  sectors['gamer'])
            db.session.add(en_sector)
            print ('sector No:' + str(en_sector.en_sector_no)+ ' sector name ' + en_sector.en_sector_name + ' closed:' + str(en_sector.en_sector_entered) + ' answer: '+ en_sector.en_sector_answer + ' gamer: ' + en_sector.en_gamer)
            try:
                db.session.commit()    
                counter +=1
                print ('sector added')
            except:
                db.session.rollback()
                print ('sector adding error')
        print ('------------------------END adding sector printing -------------------')
    #Якщо вже є сектори то перевіряємо чи кількість не змінилася
    else:
        if EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = en_lvl_id, en_lvl_no = en_lvl_no).count() != sectors_counter(sectorsJson):
            #TODO повідомлення про зміну кількості секторів
            print ('level sectors count was changed!!!')
            counter = 1
            for sector in sectorsJson:

                if EnSectors.query.filter_by(en_game_id = get_game_id(proxy_key), 
                                            en_lvl_id = en_lvl_id, 
                                            en_lvl_no = en_lvl_no, 
                                            en_sector_no = counter).all().count() == 0:
                    print ('sector was added')
                    en_sector = EnSectors(get_game_id(proxy_key), 
                                  en_lvl_id, 
                                  en_lvl_no, 
                                  counter, 
                                  sectors['name'],
                                  sectors['entered'],
                                  sectors['answer'],
                                  sectors['gamer'])
                    db.session.add(en_sector)
                    try:
                        db.session.commit()
                        counter +=1
                        print ('sector added')
                    except:
                        db.session.rollback()
                        print ('sector adding error')
    # інформація про сектори поновляється в будь якому випадку
    print ('level sectors info updating')
    counter = 1
    print ('------------------------START update sector printing -------------------')
    for sectors in sectorsJson:
        print (sectors)
        updated = False
        en_sector = EnSectors.query.filter_by(en_game_id = get_game_id(proxy_key), 
                                  en_lvl_id = en_lvl_id, 
                                  en_lvl_no = en_lvl_no, 
                                  en_sector_no = counter).first()
        print ('sector No:' + str(en_sector.en_sector_no)+ ' sector name ' + en_sector.en_sector_name + ' closed:' + str(en_sector.en_sector_entered) + ' answer: '+ en_sector.en_sector_answer + ' gamer: ' + en_sector.en_gamer)
        if sectors['name'] != en_sector.en_sector_name:
            print ('sector #' + str(counter) + ' name was changed to ' + str(sectors['name']))
            # TODO сигнал боту про зміну назви сектора
            updated = True
            en_sector.en_sector_name = sectors['name']
        if sectors ['entered'] != en_sector.en_sector_entered:
            # TODO сигнал боту про введення сектора
            print ('sector #' + str(counter) + ' name was closed by code ' + sectors['answer'] + ' by gamer '+ sectors['gamer'])
            updated = True
            en_sector.en_sector_entered = True
            en_sector.en_sector_answer = sectors['answer']
            en_sector.en_gamer = sectors['gamer']
        if updated:
            try:
                db.session.commit()
                
                print ('sector updated #' + str (counter))
            except:
                db.session.rollback()
                print ('sector updating error')
        counter +=1
    print ('------------------------END update sector printing -------------------')
    return None

def sectors_counter (sectorsJson):
    counter = 0
    for sector in sectorsJson:
        counter +=1
    return counter

def print_sectors_from_db (proxy_key, en_lvl_id, en_lvl_no):
    sectors = EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                         en_lvl_id = en_lvl_id, 
                                         en_lvl_no = en_lvl_no).all()
                                         
    print ('------------------------START DB sectors printing -------------------')
    print (sectors)                                        
    for sector in sectors:
        print ('sector No:' + str(sector.en_sector_no)+ ' sector name ' + sector.en_sector_name + ' closed:' + str(sector.en_sector_entered) + ' answer: '+ sector.en_sector_answer + ' gamer: ' + sector.en_gamer)
    print ('------------------------END DB sectors printing -------------------')
    return None

def en_task_logger (proxy_key, en_lvl_id, en_lvl_no, taskJson):
    if EnTask.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                         en_lvl_id = en_lvl_id, 
                                         en_lvl_no = en_lvl_no).count() == 0:
        print ('New task cretation')
        print (taskJson)
        en_task = EnTask (get_game_id(proxy_key), en_lvl_id, en_lvl_no, taskJson['task'])
        db.session.add(en_task)
        try:
            db.session.commit()
            print ('task added')
        except:
            db.session.rollback()
            print ('error adding task text')
    else:
        en_task = EnTask.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                          en_lvl_id = en_lvl_id, 
                                          en_lvl_no = en_lvl_no).first()
        if en_task.en_task_text != taskJson['task']:
            en_task.en_task_text = taskJson['task']
            print ('task text changed') # TODO добавити сигнал боту про зміну тексту завдання
            try:
                db.session.commit()
            except:
                db.session.rollback()
    print_task_from_db (proxy_key, en_lvl_id, en_lvl_no)
    return None

def print_task_from_db (proxy_key, en_lvl_id, en_lvl_no):
    en_task = EnTask.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                          en_lvl_id = en_lvl_id, 
                                          en_lvl_no = en_lvl_no).all()
    for task in en_task:
        print (task)
    return None

def en_prompts_loger (proxy_key, en_lvl_id, en_lvl_no, pageJson):
    prompts = json.loads(pageJson['prompts'])
    print ('prompts logger')
    print (prompts)
    # якщо немає піказок тоді вернутись
    if prompts == None: 
        return None
    # якщо не створені підказки в базі то створити їх
    if EnPrompt.query.filter_by(en_game_id = get_game_id(proxy_key), 
                                en_lvl_id = en_lvl_id, 
                                en_lvl_no = en_lvl_no).count() == 0:
        for prompt in prompts:
            if prompt['timer'] == '':
                prompt['timer'] = '0'
            en_prompt = EnPrompt (get_game_id(proxy_key), 
                                    en_lvl_id, 
                                    en_lvl_no,
                                    prompt['number'], 
                                    prompt['text'], 
                                    int(prompt['timer']))
            db.session.add (en_prompt)
            try:
                db.session.commit()
                print ('prompt added') # TODO прописати сигнали боту по підказках
            except:
                db.session.rollback()
                print ('prompt error')
    print ('prompts length =' + str (len(prompts)))
    if len(prompts) != EnPrompt.query.filter_by(en_game_id = get_game_id(proxy_key), 
                                                        en_lvl_id = en_lvl_id, 
                                                        en_lvl_no = en_lvl_no).count():
        print ('prompts count changed') # TODO сигнал боту що кількість підказок змінилася
        # перевірки чи не змінилася кількість підказок

        for prompt in prompts:
            if prompt['timer'] == '':
                    prompt['timer'] = '0'
            en_prompt = EnPrompt.query.filter_by (en_game_id = get_game_id(proxy_key),
                                                    en_lvl_id = en_lvl_id,
                                                    en_lvl_no = en_lvl_no,
                                                    en_prompt_no = prompt['number']).first()
        # якщо підказка з таким номером є то перевірити чи не змінився її текст
            if en_prompt != None:
                if en_prompt.en_prompt_text != prompt['text']:
                    # TODO подати сигнал боту що змінився текст підказки
                    en_prompt.en_prompt_text = prompt['text']
                if en_prompt.en_prompt_data != prompt['timer']:
                    # якщо час == 0 тоді додати сигнал боту про появу нової підказки
                    if prompt['timer'] == 0:
                        print ('new prompt appeared') #TODO сигнал про нову підказку
                    else:
                        # змінився час до підказки
                        print ('prompt timer changed') # TODO перезаписати сигнали боту по підказках
                    try:
                        db.session.commit()
                        print ('new prompt text written')
                    except:
                        db.session.rollback()
                        print ('error updating prompt text')
            else:
                # TODO подати сигнал боту, що додалася нова підказкка
                if prompt['timer'] == '':
                    prompt['timer'] = '0'
                en_prompt = EnPrompt (get_game_id(proxy_key), 
                                    en_lvl_id, 
                                    en_lvl_no,
                                    prompt['number'], 
                                    prompt['text'], 
                                    int(prompt['timer']))
                db.session.add (en_prompt)
                try:
                    db.session.commit()
                    print ('prompt added')
                except:
                    db.session.rollback()
                    print ('prompt error')
    print_prompts_from_db (proxy_key, en_lvl_id, en_lvl_no)
    return None

def print_prompts_from_db (proxy_key, en_lvl_id, en_lvl_no):

    en_prompt = EnPrompt.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                          en_lvl_id = en_lvl_id, 
                                          en_lvl_no = en_lvl_no).all()
    print ('------------------------START DB prompts printing -------------------')                                          
    for prompt in en_prompt:
        print (prompt)
    print ('------------------------END DB prompts printing -------------------')
    return None
                                  
def en_bonus_logger (proxy_key, en_lvl_id, en_lvl_no, pageJson):
    bonuses = json.loads (pageJson['bonuses'])
    print ('------------------------START bonus logger -------------------') 
    if len (bonuses) == 0:
        return None #якщо бонусів немає то виходимо
    if EnBonus.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                en_lvl_id = en_lvl_id, 
                                en_lvl_no = en_lvl_no).count() == 0: #якщо в базі немає бонусів тоді створюємо їх
        for bonus in bonuses:
            en_bonus = EnBonus (get_game_id(proxy_key), 
                                en_lvl_id, 
                                en_lvl_no, 
                                bonus['number'], 
                                bonus ['text'],
                                bonus['bonus_text'],
                                bonus['completed'],
                                bonus['passed'])
            db.session.add(en_bonus)
            try:
                db.session.commit()
                print ('new bonus added')
            except:
                db.session.rollback()
                print ('error adding new bonus')
    
    for bonus in bonuses:
        en_bonus = EnBonus.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                            en_lvl_id = en_lvl_id, 
                                            en_lvl_no = en_lvl_no,
                                            en_bonus_no = bonus['number']).first()
        if en_bonus == None: #якщо бонус з таким номером не знайдено значить він новий
            # TODO послати сигнал боту що додався новий бонус
            en_bonus = EnBonus (get_game_id(proxy_key), 
                                en_lvl_id, 
                                en_lvl_no, 
                                bonus['number'], 
                                bonus ['text'],
                                bonus['bonus_text'],
                                bonus['completed'],
                                bonus['passed'])
            db.session.add(en_bonus)
            try:
                db.session.commit()
                print ('new bonus added')
            except:
                db.session.rollback()
                print ('error adding new bonus')
        if en_bonus.en_bonus_text != bonus ['text']:
            # TODO послати сигнал боту що змінився текст бонусу
            en_bonus.en_bonus_text = bonus ['text']
        if en_bonus.en_bonus_prompt_text != bonus['bonus_text']:
            # TODO послати сигнал боту що змінився текст бонусної підказки
            en_bonus.en_bonus_prompt_text = bonus['bonus_text']
        if en_bonus.en_bonus_completed != bonus['completed']:
            # TODO послати сигнал боту що бонус закрився
            en_bonus.en_bonus_completed = bonus['completed']
        if en_bonus.en_bonus_passed != bonus['passed']:
            # TODO послати сигнал боту, що бонус пропустили
            en_bonus.en_bonus_passed != bonus['passed']
        try:
            db.session.commit()
            print ('bonus data updated')
        except:
            db.session.rollback()
            print ('error while updating bonus data')
    print (bonuses)
    print ('------------------------END bonus logger -------------------') 
    print_bonuses_from_db (proxy_key, en_lvl_id, en_lvl_no)
    return None

def print_bonuses_from_db (proxy_key, en_lvl_id, en_lvl_no):

    en_bonus = EnBonus.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                          en_lvl_id = en_lvl_id, 
                                          en_lvl_no = en_lvl_no).all()
    print ('------------------------START DB bonuses printing -------------------')                                          
    for bonus in en_bonus:
        print (bonus)
    print ('------------------------END DB bonuses printing -------------------')
    return None

def en_history_logger (proxy_key, en_lvl_id, en_lvl_no, pageJson):
    history = json.loads (pageJson['history'])
    if len(history) == 0:
        return None
    if len(history) != EnHistory.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                                  en_lvl_id = en_lvl_id, 
                                                  en_lvl_no = en_lvl_no).count(): #TODO аналіз введених кодів - вірний/невірний/бонус
        print ('json history len = ' + str(len(history)))
        print ('DB history count = ' + str(EnHistory.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                                                    en_lvl_id = en_lvl_id, 
                                                                    en_lvl_no = en_lvl_no).count()) )
        history_analize (proxy_key, en_lvl_id, en_lvl_no, pageJson)
        for story in history:
            if EnHistory.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                          en_lvl_id = en_lvl_id, 
                                          en_lvl_no = en_lvl_no,
                                          en_gamer = story['gamer'],
                                          en_answer = story['answer']).count() == 0:
                en_history = EnHistory (get_game_id(proxy_key), 
                                        en_lvl_id, 
                                        en_lvl_no,
                                        story['gamer'],
                                        story['answer'],
                                        story['time'],
                                        story ['is_code'],
                                        story ['correct'])
                db.session.add(en_history)
                try:
                    db.session.commit()
                    print ('history element logged')
                except:
                    db.session.rollback ()
                    print ('error loggin history')
    print_history_from_db (proxy_key, en_lvl_id, en_lvl_no)
    return None

def history_analize (proxy_key, en_lvl_id, en_lvl_no, pageJson):
    history = json.loads (pageJson['history'])
    for story in history:
        print (story)
    return None

def print_history_from_db (proxy_key, en_lvl_id, en_lvl_no):

    en_history = EnHistory.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                          en_lvl_id = en_lvl_id, 
                                          en_lvl_no = en_lvl_no).all()
    print ('------------------------START DB history printing -------------------')                                          
    for story in en_history:
        print (story)
    print ('------------------------END DB history printing -------------------')
    return None