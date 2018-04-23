import json
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from app import db
from app.game_managment import edit_game_name, get_domain, get_game_id, get_chat_tg_id
from app.models import (EnBonus, EnGame, EnHistory, EnLvl, EnPenalty, EnPrompt,
                        EnSectors, EnTask, botSignall)


def addSignal(proxyKey, type, **kwargs):
    if type == 1:
        adSignallSectorsCountChanged(get_chat_tg_id(
            proxyKey), kwargs['was'], kwargs['now'])
    if type == 2:
        adSignallSectorsCount(get_chat_tg_id(proxyKey), kwargs['now'])
    if type == 3:
        addSignallSectorNameChanged(get_chat_tg_id(
            proxyKey), kwargs['sectorNumber'], kwargs['nameOld'], kwargs['nameNew'])
    if type == 4:
        adSignallSectorClosed(get_chat_tg_id(
            proxyKey), kwargs['sectorNumber'], kwargs['sectorName'], kwargs['code'], kwargs['gamer'])
    return None


def adSignallSectorsCountChanged(chatId, was, now):
    # TODO сигнал про зміну кількості секторів тип = 1, повідоблення було was секторів, зараз now секторів, час now
    return None


def adSignallSectorsCount(chatId, now):
    # TODO сигнал про кількість секторів тип = 2, повідомлення на рівні now секторів, час now + 2 sec
    return None


def addSignallSectorNameChanged(chatId, sectorNumber, nameOld, nameNew):
    # TODO сигнад про зміну назви сектора, тип = 3, повідомлення: назва сектора № sectorNumber змінилася з nameOld, nameNew, час now
    return None


def adSignallSectorClosed(chatId, sectorNumber, sectorName, code, gamer):
    # TODO сигнал про введення сектора, тип = 4, повідомлення сектор № sectorNumber, закритий кодом code, гравцем gamer, час now
    return None
