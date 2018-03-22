import json
import time
from bs4 import BeautifulSoup
from datetime import datetime


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
history_class = 'history'
correct_answer_class ='color_correct'
correct_bonus_class = 'color_bonus'
sectors_div_class = 'cols-wrapper'
content_div_class = 'content'

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
    print (get_level_num (soup))
    print (get_level_history (soup))
    if have_sectors (soup):
        get_sectors (soup)
    return page

def get_level_num (pageSoup):
    """
    отримує суп сторінки гри, повертає json:
    {'levelId':id рівня в ігровій системі,
    'levelNum':номер рівня в ігрі}
    """
    inputs = pageSoup.find('form').findAll('input')
    for input_ in inputs:
        if input_.has_attr('name'):
            if input_['name'] == level_id_name:
                level_id = input_['value']
            if input_['name'] == level_number_name:
                level_num = input_['value']
    print (level_id, level_num)
    return json.dumps ( {'levelId':level_id,
                    'levelNum':level_num })

def get_level_history (pageSoup):
    """
    отримує суп сторінки гри повертає історію вводу кодів в форматі json
    'time': юнікс тайм введення коду
    'gamer': гравець який ввів код
    'answer': код
    'correct': вірний/невірий код (True/False)
    'is_code': якщо True то був введений код, інакше бонус
    """
    history = []
    history_list = pageSoup.find('ul', class_=history_class)
    items = history_list.findAll('li')
    for item in items:
        code_date = get_code_date(item.get_text().strip())
        #code_date = code_date[0:code_date.find('/n')]
        user = item.find('a').get_text().strip()
        answer = item.find('span').get_text().strip()
        answer_class = item.find('span')['class']
        if  answer_class[0] == correct_answer_class:
            correct = True
            isCode = True
        else:
            if answer_class[0] == correct_bonus_class:
                correct = True
                isCode = False
            else:
                correct = False
                isCode = True

        history.append ({'time':code_date,'gamer':user,'answer':answer,'correct':correct,'is_code':isCode})
    return json.dumps(history)

def have_sectors (pageSoup):
    """
    отримує суп сторінки гри і повертає True якщо на рівні є сектори
    """
    try:
        sectors = pageSoup.findAll('div', class_=sectors_div_class)
        if len(sectors) > 0:
            return True
        else:
            return False
    except:
        return False

def get_sectors (pageSoup):
    content = pageSoup.find ('div', class_ = content_div_class)
    sectors_count = content.findAll ('h3')[0]
    i = 0
    for s in sectors_count.get_text().split():
        if s.isdigit():
            i += 1
            if i == 1:
                print ('sectors all ='+s)
                all_sectors = s
            else:
                print ('sectors need ='+s)
                need_sectors = s
    #sectors = pageSoup.findFirst('h3')
    print (sectors_count)
    return 1

def get_code_date(inStr):
    tmp_date_str = str(datetime.now().year)+'/'+inStr.split()[0]+' '+ inStr.split()[1]
    tmp_date_str = tmp_date_str.replace ('/', ' ')
    date = datetime.strptime (tmp_date_str, '%Y %d %m %H:%M:%S')
    return time.mktime (date.timetuple())
