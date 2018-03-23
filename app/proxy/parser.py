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
code_not_entered_class = 'color_dis'
code_entered_class = 'color_correct'
spacer = 'spacer'

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
        print(get_sectors_count (soup))
        print (get_sectors_info (soup))
    print(get_task(soup))
    get_prompts (soup)
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

def get_sectors_count (pageSoup):
    """
    отримує суп сторінки гри повертає json:
    'all': всього секторів на рівні
    'need': потрібно для закриття рівня
    """
    content = pageSoup.find ('div', class_ = content_div_class)
    sectors_count = content.findAll ('h3')[0]
    sectors_span = sectors_count.findAll('span')[0].get_text()
    sectors_span = sectors_span.replace (')','')
    sectors_all = [str(s) for s in sectors_count.get_text().split() if s.isdigit()][0]
    sectors_need = [str(s) for s in sectors_span.split() if s.isdigit()][0]
    return json.dumps({'all':sectors_all,'need':sectors_need})

def get_sectors_info(pageSoup):
    """
    отримує суп сторінки повертає json:
    'name': назва сектору
    'entered': True якщо сектор закритий
    'answer': введений код
    'gamer': логін гравця, що закрив код
    """
    sectors =pageSoup.find('div', class_=sectors_div_class).findAll('p')
    sectors_list=[]
    for sector in sectors:
        name =sector.get_text().split(':')[0].strip()
       
        for code in sector.findAll('span'):
            
            if code['class'][0] == code_not_entered_class:
                entered = False
                answer = ''
                gamer = ''
            else:
                if code['class'][0] == code_entered_class:
                    entered = True
                    answer = code.get_text().strip()
                    
                else:
                    gamer = code.findAll('a')[0].get_text().strip()
                    
        sectors_list.append({'name':name,'entered':entered,'answer':answer,'gamer':gamer})            
    return json.dumps (sectors_list)

def get_task(pageSoup):
    """
    отримує суп сторінки повертає json
    'task': повний текст завдання
    """
   
    content = pageSoup.find('div', class_ = content_div_class)
    #print (set_block(content.prettify()))
    #content = content.div(class_ = spacer)
    #content = content.div.next_siblings()
    blocks = BeautifulSoup (set_block(content.prettify()))
    task = blocks.find('div', class_ = 'block_task')
    return json.dumps ({'task':str(task)})

def get_prompts (pageSoup):
    content = pageSoup.find('div', class_ = content_div_class)
    blocks = BeautifulSoup (set_block(content.prettify()))
    prompts = blocks.findAll('div', class_ = 'block_prompt')
    for prompt in prompts:
        if len(prompt.findAll('span', class_ = code_not_entered_class)) != 0:
            get_timer (prompt.prettify())
            print (prompt)
    return 1

def get_timer (html):
    timer = BeautifulSoup (html)
    timer = timer.find ('script')
    timer = json.loads (timer.get_text())
    timer = timer ['StartCounter']
    print (timer)
    return 1

def set_block (html):
    i=1
    first = True
    html_dic = html.split('\n')
    for z in range(0, len(html_dic)-1):
        
        if html_dic[z].strip() == '<div class="'+spacer+'">' and i==1:
            html_dic[z] = '<div class="block">'
            if first:
                html_dic[z+1] ='' 
                first = False
            else:
                html_dic[z] = '</div>'
                html_dic[z+1] ='<div class="block">'

            i += 1
        if html_dic[z].strip() == '<div class="'+spacer+'">' and i == 2:
            html_dic[z] = '</div>' 
            html_dic[z+1] ='<div class="block">'
            i = 1
    html_dic = rename_block (html_dic)   
    html = ''.join(html_dic)
    return html

def rename_block (html_dic):
    counter = 0
    for z in range(0, len(html_dic)-1):
        if html_dic[z] == '<div class="block">' and counter == 0:
            html_dic[z] = '<div class="block_sectors">' 
            counter = 1
        if html_dic[z] == '<div class="block">' and counter == 1:
            html_dic[z] = '<div class="block_task">' 
            counter = 2
        if html_dic[z] == '<div class="block">' and counter == 2:
           html_dic[z] = '<div class="block_prompt">' 
           counter = 2
        if html_dic[z] == '<div class="block">' and html_dic[z+1].strip() == '<h3 class="'+correct_bonus_class+'">' or html_dic[z+1].strip() == '<h3 class="'+code_entered_class+'">':
           html_dic[z] = '<div class="block_bonus">' 
           counter = 3
    return html_dic



def get_code_date(inStr):
    # ValueError: time data '2018 4:29:58 PM' does not match format '%Y %d %m %H:%M:%S'
    tmp_date_str = str(datetime.now().year)+'/'+inStr.split()[0]+' '+ inStr.split()[1]
    tmp_date_str = tmp_date_str.replace ('/', ' ')
    try:
        date = datetime.strptime (tmp_date_str, '%Y %d %m %H:%M:%S')
    except:
        return 0
    return time.mktime (date.timetuple())
