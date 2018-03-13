from bs4 import BeautifulSoup

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

def s(page, id):
    soup = BeautifulSoup(page.text).prettify()
    a = soup.a
    a['href']= '/proxy/'+id+'/'+a['href']
    print (soup)
    return soup
