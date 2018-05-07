import json
import time
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from app import db
from app.game_managment import edit_game_name, get_domain, get_game_id, get_chat_tg_id
from app.models import (EnBonus, EnGame, EnHistory, EnLvl, EnPenalty, EnPrompt,
                        EnSectors, EnTask, botSignall)
from app.bot.messages import *


def addSignal(proxyKey, type_, **kwargs):
    print_signals()
    print ('signal type = '+ str(type_))
    if type_ == 1:
        adSignallSectorsCountChanged(get_chat_tg_id(
            proxyKey), kwargs['was'], kwargs['now'], kwargs['level'])
    if type_ == 2:
        adSignallSectorsCount(get_chat_tg_id(proxyKey), kwargs['now'], kwargs['level'])
    if type_ == 3:
        addSignallSectorNameChanged(get_chat_tg_id(
            proxyKey), kwargs['sectorNumber'], kwargs['nameOld'], kwargs['nameNew'])
    if type_ == 4:
        adSignallSectorClosed(get_chat_tg_id(
            proxyKey), kwargs['sectorNumber'], kwargs['sectorName'], kwargs['code'], kwargs['gamer'])
    if type_ == 5:
        adSignallNewTask(get_chat_tg_id(proxyKey),
                         kwargs['level'], kwargs['task'])
    if type_ == 6:
        adSignallTask(get_chat_tg_id(proxyKey),
                      kwargs['level'], kwargs['task'])
    if type_ == 7:
        addSignallTaskChanged(get_chat_tg_id(proxyKey),
                              kwargs['level'], kwargs['task'])
    if type_ == 8:
        addSignallPromptsCount(get_chat_tg_id(proxyKey),
                               kwargs['level'], kwargs['count'])
    if type_ == 9:
        print ('Signal type 9 !!!!!!!!!!!!!!!!!!!!')
        addSignalRenew(proxyKey, kwargs['timestamp'])
    if type_ == 10:
        addSignalPromptsCountChanged(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['oldCount'], kwargs['newCount'])
    if type_ == 11:
        addSignallPromptTextChanged(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'])
    if type_ == 12:
        
        addSignallPromptNew(get_chat_tg_id(proxyKey),
                            kwargs['level'], kwargs['number'], kwargs['text'])
    if type_ == 13:
        addSignallPenaltyPromptsCount(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['count'])
    if type_ == 14:
        addSignalPenaltyPromptsCountChanged(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['oldCount'], kwargs['newCount'])
    if type_ == 15:
        addSignallPenaltyPromptNew(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'])
    if type_ == 16:
        addSignallBonusCount (get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['count'])
    if type_ == 17:
        addSignallBonusText(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'], kwargs['bonus_text'])
    if type_ == 18:
        addSignallBonusNew(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'], kwargs['bonus_text'])
    if type_ == 19:
        addSignallBonusTextNew(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'], kwargs['bonus_text'])
    if type_ == 20:
        addSignallBonusClosed(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'], kwargs['bonus_text'], kwargs['answer'], kwargs['gamer'])
    if type_ == 21:
        addSignallBonusPassed(get_chat_tg_id(
            proxyKey), kwargs['level'], kwargs['number'], kwargs['text'], kwargs['bonus_text'])
    return None


def adSignallSectorsCountChanged(chatId, was, now, level):
    # TODO сигнал про зміну кількості секторів тип = 1, повідоблення було was секторів, зараз now секторів, час now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 1
    signal.level = level
    signal.signal_json = json.dumps ({'msg':sectors_count_changed_msg.format(was, now), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Sectors count changed signall commited')
    except:
        db.session.rollback()
        print ('Sectors count changed signall NOT commited')
    return None


def adSignallSectorsCount(chatId, now, level):
    # TODO сигнал про кількість секторів тип = 2, повідомлення на рівні now секторів, час now + 1 sec
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 2
    signal.level = level
    signal.signal_json = json.dumps ({'msg':sectors_count_msg.format(now), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())+1
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Sectors count signall commited')
    except:
        db.session.rollback()
        print ('Sectors count signall NOT commited')
    return None


def addSignallSectorNameChanged(chatId, sectorNumber, nameOld, nameNew, level):
    # TODO сигнад про зміну назви сектора, тип = 3, повідомлення: назва сектора № sectorNumber змінилася з nameOld, nameNew, час now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 3
    signal.level = level
    signal.signal_json = json.dumps ({'msg':sector_renamed_msg.format(sectorNumber, nameOld, nameNew), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Sectors renamed signall commited')
    except:
        db.session.rollback()
        print ('Sectors renamed signall NOT commited')
    return None


def adSignallSectorClosed(chatId, sectorNumber, sectorName, code, gamer, level):
    # TODO сигнал про введення сектора, тип = 4, повідомлення сектор № sectorNumber, закритий кодом code, гравцем gamer, час now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 4
    signal.level = level
    if sectorName =='':
        signal.signal_json = json.dumps ({'msg':sector_noname_closed_msg.format(sectorNumber, code, gamer), 'html':''})
    else:
        signal.signal_json = json.dumps ({'msg':sector_named_closed_msg.format(sectorName, code, gamer), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Sectors closed signall commited')
    except:
        db.session.rollback()
        print ('Sectors closed signall NOT commited')
    return None


def adSignallNewTask(chatId, level, task):
    # TODO сигнал про нове завдання тип = 5, повідомлення: Перехід на новий рівень level, отримано завдання. task, час =now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 5
    signal.level = level
    signal.signal_json = json.dumps ({'msg':new_level_msg.format(level), 'html':task})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New task signall commited')
    except:
        db.session.rollback()
        print ('new task signall NOT commited')    
    return None


def adSignallTask(chatId, level, task):
    # TODO сигнал перевідправку завдання тип = 6, повідомлення: Завдання рівня level. task, час =now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 6
    signal.level = level
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Reload signall commited')
    except:
        db.session.rollback()
        print ('Reload signall NOT commited')      
    return None


def addSignallTaskChanged(chatId, level, task):
    # TODO сигнал про зміну завдання тип = 7, повідомлення: Текст завдання рівня№ level змінився. Task, час = now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 7
    signal.level= level
    signal.signal_json = json.dumps ({'msg':task_changed_msg, 'html':task})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Task changed signall commited')
    except:
        db.session.rollback()
        print ('Task changed signall NOT commited') 
    return None


def addSignallPromptsCount(chatId, level, count):
    # TODO сигнал боту про кількість підказок, тип = 8, повідомлення: на рівні № level count підказок, час = now +2
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 8
    signal.level = level
    signal.signal_json = json.dumps ({'msg':prompts_count_msg.format(count), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple()) + 2
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Prompts  count signall commited')
    except:
        db.session.rollback()
        print ('Prompts count signall NOT commited')     
    return None


def addSignalRenew(proxyKey, timestamp):
    # TODO сигнал проксі поновити сторінку тип = 9, на проксі proxyKey, в час timestamp
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 9
    signal.signal_json = json.dumps ({'msg':proxyKey, 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    signal.level = 0
    print ('renew signal try to add')
    print (signal)
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Renew signall commited')
    except:
        db.session.rollback()
        print ('Renew signall NOT commited')  
    return None


def addSignalPromptsCountChanged(chatId, level, oldCount, newCount):
    # TODO сигнал боту, що змінилася кількість підказок тип = 10, повідомлення: на рівні № level змінилася в кількість підказок з oldCount на newCount, час now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 10
    signal.level = level
    signal.signal_json = json.dumps ({'msg':prompts_count_changed_msg.format(level, oldCount, newCount), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Renew signall commited')
    except:
        db.session.rollback()
        print ('Renew renamed signall NOT commited')  
    return None


def addSignallPromptTextChanged(chatId, level, number, text):
    # TODO сигнал боту що змінився текст підказки, тип =11, повідомлення: на рівні № level змінився текст підказки № number на text, час = now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 11
    signal.level = level
    signal.signal_json = json.dumps ({'msg':prompt_text_changed_msg.format(level, number), 'html':text})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Prompt Text Changed signall commited')
    except:
        db.session.rollback()
        print ('Prompt Text Changed signall NOT commited') 
    return None


def addSignallPromptNew(chatId, level, number, text):
    # TODO сигнал боту про появу нової підказки, тип = 12, повідомлення: на рівні № level з'явилася нова підказка № number : text, час = now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 12
    signal.level = level
    signal.signal_json = json.dumps ({'msg':new_prompt_msg.format(number), 'html':text})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New prompt signall commited')
    except:
        db.session.rollback()
        print ('New prompt signall NOT commited') 
    return None    



def addSignallPenaltyPromptsCount(chatId, level, count):
    # TODO сигнал боту про кількість штрафних підказок, тип = 13, повідомлення: на рівні № level count штрафних підказок, час = now +3
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 13
    signal.level = level
    signal.signal_json = json.dumps ({'msg':penalty_count_msg.format(count), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())+3
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New prompt signall commited')
    except:
        db.session.rollback()
        print ('New prompt signall NOT commited') 
    return None


def addSignalPenaltyPromptsCountChanged(chatId, level, oldCount, newCount):
    # TODO сигнал боту, що змінилася кількість штрафних підказок тип = 14, повідомлення: на рівні № level змінилася в кількість штрафних підказок з oldCount на newCount, час now
    signal = botSignall()
    signal.chat_id = chatId
    signal.signal_type = 14
    signal.level = level
    signal.signal_json = json.dumps ({'msg':penalty_count_changed_msg .format(level,oldCount, newCount), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New prompt signall commited')
    except:
        db.session.rollback()
        print ('New prompt signall NOT commited')     
    return None


def addSignallPenaltyPromptNew(chatId, level, number, text):
    # TODO сигнал боту про появу штрафної нової підказки, тип = 15, повідомлення: на рівні № level з'явилася нова штрафна підказка № number : text, час = now
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 15
    signal.level = level
    signal.signal_json = json.dumps ({'msg':new_penalty_prompt_msg.format(level,number), 'html':text})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New prompt signall commited')
    except:
        db.session.rollback()
        print ('New prompt signall NOT commited')      
    return None


def addSignallBonusCount(chatId, level, count):
    # TODO сигнал боту про кількість бонусів, тип = 16, повідомлення: на рівні № level count бонусів, час = now +4
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 16
    signal.level = level
    signal.signal_json = json.dumps ({'msg':bonus_count_msg.format(level,count), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())+4
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Bonus count signall commited')
    except:
        db.session.rollback()
        print ('Bonus count signall NOT commited')   
    return None


def addSignallBonusText(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про текст бонусу, тип = 17, повідомлення: Бонус № number на рівні № level, text , bonus_text , now +5
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 17
    signal.level = level
    signal.signal_json = json.dumps ({'msg':bonus_text_msg.format(level,number), 'html':text})
    signal.signal_date = time.mktime(datetime.now().timetuple())+5
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Bonus text signall commited')
    except:
        db.session.rollback()
        print ('Bonus text signall NOT commited')     
    return None




def addSignallBonusNew(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про появу нового бонусу, тип = 18, повідомлення: на рівні № level з'явився новий бонус № number : text, bonus_text, час = now
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 18
    signal.level = level
    signal.signal_json = json.dumps ({'msg':new_bonus_text_msg.format(level,number), 'html':text})
    signal.signal_date = time.mktime(datetime.now().timetuple())+5
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New Bonus signall commited')
    except:
        db.session.rollback()
        print ('New Bonus signall NOT commited')    
    return None


def addSignallBonusTextNew(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про текст бонусу, тип = 19, повідомлення: Бонус № number на рівні № level змінився, text , bonus_text , час = now
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 19
    signal.level = level
    signal.signal_json = json.dumps ({'msg':bonus_text_changed.format(level,number), 'html':text})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('New Bonus text signall commited')
    except:
        db.session.rollback()
        print ('New Bonus text signall NOT commited')     
    return None


def addSignallBonusClosed(chatId, level, number, text, bonus_text, answer, gamer):
    # TODO сигнал боту про закриття, тип = 20, повідомлення: Бонус № number на рівні № level закрито гравцем gamer, кодом answer, отримано бонусну підказку bonus_text , час = now
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 20
    signal.level = level
    signal.signal_json = json.dumps ({'msg':bonus_answered_msg.format(level,number, gamer, answer), 'html':text+bonus_text})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Bonus answered text signall commited')
    except:
        db.session.rollback()
        print ('Bonus answered text signall NOT commited')      
    return None


def addSignallBonusPassed(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про пропуск, тип = 21, повідомлення: Бонус № number на рівні № level пропущено , час = now
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 21
    signal.level = level
    signal.signal_json = json.dumps ({'msg':bonus_passed_msg.format(level,number), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Bonus answered text signall commited')
    except:
        db.session.rollback()
        print ('Bonus answered text signall NOT commited') 
    return None

def print_signals():
    signals = botSignall.query.all()
    print ('------------------ START PRINTING SIGNAL ---------------------')
    for signall in signals:
        print (signall)
    print ('------------------ END PRINTING SIGNAL ---------------------')
    return None


def addSignallUpTime (chatId, level, timer):
    # TODO сигнал боту про ап, тип = 22, повідомлення: Час до Апу , час = now-1
    signal = botSignall()    
    signal.chat_id = chatId
    signal.signal_type = 22
    signal.level = level
    time_up = time.strftime("%H:%M:%S", time.gmtime(timer - time.mktime(datetime.now().timetuple())))
    signal.signal_json = json.dumps ({'msg':up_msg.format(time_up), 'html':''})
    signal.signal_date = time.mktime(datetime.now().timetuple())-1
    db.session.add(signal)
    try:
        db.session.commit()
        print ('Bonus answered text signall commited')
    except:
        db.session.rollback()
        print ('Bonus answered text signall NOT commited') 
    return None
        
