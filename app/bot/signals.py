import json
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from app import db
from app.game_managment import edit_game_name, get_domain, get_game_id, get_chat_tg_id
from app.models import (EnBonus, EnGame, EnHistory, EnLvl, EnPenalty, EnPrompt,
                        EnSectors, EnTask, botSignall)


def addSignal(proxyKey, type_, **kwargs):
    if type_ == 1:
        adSignallSectorsCountChanged(get_chat_tg_id(
            proxyKey), kwargs['was'], kwargs['now'])
    if type_ == 2:
        adSignallSectorsCount(get_chat_tg_id(proxyKey), kwargs['now'])
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
        addSignallBonusCountCount(get_chat_tg_id(
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


def adSignallSectorsCountChanged(chatId, was, now):
    # TODO сигнал про зміну кількості секторів тип = 1, повідоблення було was секторів, зараз now секторів, час now
    return None


def adSignallSectorsCount(chatId, now):
    # TODO сигнал про кількість секторів тип = 2, повідомлення на рівні now секторів, час now + 1 sec
    return None


def addSignallSectorNameChanged(chatId, sectorNumber, nameOld, nameNew):
    # TODO сигнад про зміну назви сектора, тип = 3, повідомлення: назва сектора № sectorNumber змінилася з nameOld, nameNew, час now
    return None


def adSignallSectorClosed(chatId, sectorNumber, sectorName, code, gamer):
    # TODO сигнал про введення сектора, тип = 4, повідомлення сектор № sectorNumber, закритий кодом code, гравцем gamer, час now
    return None


def adSignallNewTask(chatId, level, task):
    # TODO сигнал про нове завдання тип = 5, повідомлення: Перехід на новий рівень level, отримано завдання. task, час =now
    return None


def adSignallTask(chatId, level, task):
    # TODO сигнал перевідправку завдання тип = 6, повідомлення: Завдання рівня level. task, час =now
    return None


def addSignallTaskChanged(chatId, level, task):
    # TODO сигнал про зміну завдання тип = 7, повідомлення: Текст завдання рівня№ level змінився. Task, час = now
    return None


def addSignallPromptsCount(chatId, level, count):
    # TODO сигнал боту про кількість підказок, тип = 8, повідомлення: на рівні № level count підказок, час = now +2
    return None


def addSignalRenew(proxyKey, timestamp):
    # TODO сигнал проксі поновити сторінку тип = 9, на проксі proxyKey, в час timestamp
    return None


def addSignalPromptsCountChanged(chatId, level, oldCount, newCount):
    # TODO сигнал боту, що змінилася кількість підказок тип = 10, повідомлення: на рівні № level змінилася в кількість підказок з oldCount на newCount, час now
    return None


def addSignallPromptTextChanged(chatId, level, number, text):
    # TODO сигнал боту що змінився текст підказки, тип =11, повідомлення: на рівні № level змінився текст підказки № number на text, час = now
    return None


def addSignallPromptNew(chatId, level, number, text):
    # TODO сигнал боту про появу нової підказки, тип = 12, повідомлення: на рівні № level з'явилася нова підказка № number : text, час = now
    return None


def addSignallPenaltyPromptsCount(chatId, level, count):
    # TODO сигнал боту про кількість штрафних підказок, тип = 13, повідомлення: на рівні № level count штрафних підказок, час = now +3
    return None


def addSignalPenaltyPromptsCountChanged(chatId, level, oldCount, newCount):
    # TODO сигнал боту, що змінилася кількість штрафних підказок тип = 14, повідомлення: на рівні № level змінилася в кількість штрафних підказок з oldCount на newCount, час now
    return None


def addSignallPenaltyPromptNew(chatId, level, number, text):
    # TODO сигнал боту про появу нової підказки, тип = 15, повідомлення: на рівні № level з'явилася нова штрафна підказка № number : text, час = now
    return None


def addSignallBonusCount(chatId, level, count):
    # TODO сигнал боту про кількість бонусів, тип = 16, повідомлення: на рівні № level count бонусів, час = now +4
    return None


def addSignallBonusText(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про текст бонусу, тип = 17, повідомлення: Бонус № number на рівні № level, text , bonus_text , now +5
    return None


def addSignallBonusNew(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про появу нового бонусу, тип = 18, повідомлення: на рівні № level з'явився новий бонус № number : text, bonus_text, час = now
    return None


def addSignallBonusTextNew(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про текст бонусу, тип = 19, повідомлення: Бонус № number на рівні № level змінився, text , bonus_text , час = now
    return None


def addSignallBonusClosed(chatId, level, number, text, bonus_text, answer, gamer):
    # TODO сигнал боту про закриття, тип = 20, повідомлення: Бонус № number на рівні № level закрито гравцем gamer, кодом answer, отримано бонусну підказку bonus_text , час = now
    return None


def addSignallBonusPassed(chatId, level, number, text, bonus_text):
    # TODO сигнал боту про пропуск, тип = 21, повідомлення: Бонус № number на рівні № level пропущено , час = now
    return None
