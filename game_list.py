import requests
from flask import request
from parser import game_info_list

def get_game_list(id):
    gamesSession = requests.Session()
    url ="http://127.0.0.1:5000/"+id
    print (url)
    page = gamesSession.get (url)
    print (url)

    return game_info_list (page)
