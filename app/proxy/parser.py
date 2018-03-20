from bs4 import BeautifulSoup
from flask import jsonify

"""
left_panel_tag ='tdContentLeft'
header_tag = 'tableHeader'
right_panel_tag ='tdContentRight'
main_manu_tag = 'menuWrap'
info_block ='boxCenterContent'
vote_class ='enPnl1 border_rad2 clr2'
discuss_class ='discuss'
game_info_class =  'lnkGameTitle' #'boxGameInfo' 'yellow_darkgreen19'
game_info_table_class = 'gameInfo'
"""

game_name_id = 'lnkGameTitle'
game_start_time_id = 'ComingGamesRepeater_ctl00_gameInfo_enContPanel_lblYourTime'
game_description_class = 'divDescr'
level_id_name = 'LevelId'
level_number_name = 'LevelNumber'

def get_game_info(page):
    soup = BeautifulSoup(page.text)
    name =soup.find('a', id = game_name_id).get_text()

    #soup = BeautifulSoup(page.text)
    #time = soup.find('span', id = game_start_time_id).get_text()
#    soup = BeautifulSoup(page.text)
#    description = soup.find ('div', class_ = game_description_class).prettify()
#    info = {'name':name,'description':description}
    
    print (soup.prettify())
    
    return name

def change_href (page, id):
    soup = BeautifulSoup(page.text)
    soup.prettify()
    for ref in soup.findAll('a', href=True):
        if ref['href'][0] == '/':
            ref['href'] = '/proxy/'+str(id)+ref['href']
    for ref in soup.findAll('a', href=True):
        print (ref['href'])
    return soup.prettify()

def level_parser (page):
    soup = BeautifulSoup(page)
    soup.prettify()
    inputs = soup.find.('form').findAll('input', hidden = True)
    for input_ in inputs:
        """
        if input_['name'] == level_id_name:
            level_id = input_.get_text()
        if input_['name'] == level_number_name:
            level_num = input_.get_text()
        """
        print (input_)
    #print (level_id, level_num)

    return page
