import json
import time
from app import db
from app.models import EnGameJson
from sqlalchemy.orm import sessionmaker
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
timer_marker_js = '"StartCounter":'
timer_class ='timer'
penalty_h3_class = 'inline'
answer_block_div_class ='hint blockageinfo'

def get_game_info(page):
    soup = BeautifulSoup(page.text, "lxml")
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
    try:
        soup.find('div', class_ = "header").replaceWith('')
    except:
        print ('гра ще не почалася')
    for ref in soup.findAll('a', href=True):
        if ref['href'][0] == '/':
            ref['href'] = '/proxy/'+str(id)+ref['href']
    for ref in soup.findAll('a', href=True):
        print (ref['href'])
    return soup.prettify()

def level_parser (page):
    soup = BeautifulSoup(page)
    soup.prettify()
    try:
        levelInfo = get_level_num (soup)
    except:
        return {'html':page,'json':'{game:None}'}
    history = get_level_history (soup)
    time_up = get_up (soup)
    if have_sectors (soup):
        sectors_count = get_sectors_count (soup)
        sectors_info = get_sectors_info (soup)
    else:
        sectors_count = json.dumps({'all':1,'need':1})
        sectors_info = json.dumps ({'name':'1','entered':False,'answer':'','gamer':''}
    soup = BeautifulSoup(page)
    soup.prettify()
    task = get_task(soup)
    prompts = get_prompts (soup)
    bonuses = get_bonuses (soup)
    level ={'levelinfo':levelInfo,
                        'block': get_blockage_info (soup),
                        'history':history, 
                        'up':time_up,
                        'sectors_count':sectors_count, 
                        'sectors_info':sectors_info,
                        'task':task,
                        'prompts':prompts,
                        'penalty':get_penalty (soup),
                        'bonuses':bonuses}
    #print (level)
    dbJson = EnGameJson(str(level))
    #dbJson.json = 
    db.session.add (dbJson)
    try:
        db.session.commit()
    #    print ('added')
    except:
        db.session.rollback()
        print ('not added')
    #for result in EnGameJson.query.all():
    #    print (result)
    return {'html':set_block (page),'json':level}

def get_blockage_info (pageSoup):
    if len(pageSoup.findAll('div', class_ = answer_block_div_class))>0:
        return True
    else:
        return False


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
    #1522082148.0
    try:
        content.find ('h3', class_= timer_class).replaceWith('')
    except:
        pass
    sectors_count = content.findAll ('h3')[0]
    try:
        sectors_span = sectors_count.findAll('span')[0].get_text()
        sectors_span = sectors_span.replace (')','')
        sectors_all = [str(s) for s in sectors_count.get_text().split() if s.isdigit()][0]
        sectors_need = [str(s) for s in sectors_span.split() if s.isdigit()][0]
        return json.dumps({'all':sectors_all,'need':sectors_need})
    except:
        sectors_all = [str(s) for s in sectors_count.get_text().split() if s.isdigit()][0] 
        return json.dumps({'all':sectors_all,'need':sectors_all})

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
    blocks = BeautifulSoup (set_block(content.prettify()))
    task = blocks.find('div', class_ = 'block_task')
    #print ('task = '+ str(blocks))
    return json.dumps ({'task':str(task)})

def get_prompts (pageSoup):
    """
    отримує суп сторінки повертає json
    'number': номер підказки
    'text': хтмл підказки
    'timer': час до появи підказки
    """
    content = pageSoup.find('div', class_ = content_div_class)
    blocks = BeautifulSoup (set_block(content.prettify()))
    prompts = blocks.findAll('div', class_ = 'block_prompt')
    counter = 0
    jprompt = []
    for prompt in prompts:
        counter +=1
        if len(prompt.findAll('span', class_ = code_not_entered_class)) != 0:
            if str(prompt).find('Penalty') < 0:
                jprompt.append ({'number':counter, 'text':'', 'timer':get_timer (prompt.prettify())})
        else:
            jprompt.append ({'number':counter, 'text':str(prompt), 'timer':''})
    return json.dumps(jprompt)

def get_penalty (pageSoup):
    """
    отримує суп сторінки повертає json
    'number': номер підказки
    'text': хтмл підказки
    'timer': час до появи підказки
    """
    content = pageSoup.find('div', class_ = content_div_class)
    blocks = BeautifulSoup (set_block(content.prettify()))
    prompts = blocks.findAll('div', class_ = 'block_penalty')
    counter = 0
    jprompt = []
    for prompt in prompts:
        counter +=1
        if len(prompt.findAll('span', class_ = code_not_entered_class)) != 0:
            if str(prompt).find('Penalty') > 0:
                jprompt.append ({'number':counter, 'text':'', 'timer':get_timer (prompt.prettify())})
        else:
            jprompt.append ({'number':counter, 'text':str(prompt), 'timer':''})
    prompts = blocks.findAll('div', class_ = 'block_prompt')
    for prompt in prompts:
        counter +=1
        if len(prompt.findAll('span', class_ = code_not_entered_class)) != 0:
            if str(prompt).find('Penalty') > 0:
                jprompt.append ({'number':counter, 'text':'', 'timer':get_timer (prompt.prettify())})
    return json.dumps(jprompt)


def get_bonuses (pageSoup):

    content = pageSoup.find('div', class_ = content_div_class)
    blocks = BeautifulSoup (set_block(content.prettify()))
    bonuses = blocks.findAll('div', class_ = 'block_bonus')
    counter = 0
    jbonus = []
    for bonus in bonuses:
        counter +=1
        if len(bonus.findAll('span', class_ = code_not_entered_class)) != 0:
            jbonus.append ({'number':counter, 'text':'','bonus_text':'', 'completed':False, 'passed':True})
        else:
            if len (bonus.findAll('h3', class_ = code_entered_class)) != 0:
                if len (bonus.findAll('p')) != 0:
                    jbonus.append ({'number':counter, 'text':str(bonus.h3),'bonus_text':str(bonus.p), 'completed':True, 'passed':False})
                else:
                    jbonus.append ({'number':counter, 'text':str(bonus.h3),'bonus_text':'', 'completed':True, 'passed':False})
            else:
                jbonus.append ({'number':counter, 'text':str(bonus),'bonus_text':'', 'completed':False, 'passed':False})
    return json.dumps(jbonus)

def get_up (pageSoup):
    try:
        content = pageSoup.find ('h3', class_= timer_class)
        return get_timer (content.prettify())
    except:
        print ('get_up() up not found')
        return str(time.mktime (datetime.now().timetuple()))
    

def get_timer (html):
    """
    отримує хтмл з тегом script витягує із скрипта час до підказки і повертає юнікстайм
    """
    timer = BeautifulSoup (html)
    timer = timer.find ('script')
    timer = timer.get_text()
    tmp = timer [timer.find(timer_marker_js)+len(timer_marker_js):len(timer)]
    tmp = tmp.split(',')[0]
    unixtime = int(time.mktime (datetime.now().timetuple()))+int (tmp)
    return str(unixtime) 

def set_block (html):
    """
    отримує стрінг хтмл із движка(div.content), 
    ділить контент на боки <div class= "block"> по класах з движка <div class="spacer">
    """
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
    """
    отримує стрінг хтмл переробений на блоки, визначає тип коного блоку:
    block_sectors
    block_timer
    block_task
    block_bonus
    block_prompt
    block_penalty
    """
    counter = 0
    penalty = False
    for z in range(0, len(html_dic)-1):
        if html_dic[z] == '<div class="block">' and counter == 0:
            #print ('next block =' +html_dic[z+2].strip())
            if html_dic[z+2].strip()!='<h3 class="'+timer_class+'">':
                html_dic[z] = '<div class="block_sectors">' 
                counter = 1
            else:
                html_dic[z] = '<div class="block_timer">'

        if html_dic[z] == '<div class="block">' and counter == 1:
            html_dic[z] = '<div class="block_task">' 
            counter = 2
        if html_dic[z] == '<div class="block">' and counter == 2:
          if html_dic[z+1].strip() != '<h3 class="'+penalty_h3_class+'">':
                if penalty:
                   html_dic[z] = '<div class="block_penalty">' 
                html_dic[z] = '<div class="block_prompt">'
                counter = 2
          else:
                html_dic[z] = '<div class="block_penalty">'
                penalty = True
                counter = 2
        if html_dic[z] == '<div class="block">' and html_dic[z+1].strip() == '<h3 class="'+correct_bonus_class+'">' or html_dic[z+1].strip() == '<h3 class="'+code_entered_class+'">':
           html_dic[z] = '<div class="block_bonus">' 
           
           counter = 3
        if html_dic[z] == '<div class="block">' and html_dic[z+1].strip() == '<span class="'+code_not_entered_class+'">' and counter == 3:
            html_dic[z] = '<div class="block_bonus">'
    return html_dic



def get_code_date(inStr):
    # ValueError: time data '2018 4:29:58 PM' does not match format '%Y %d %m %H:%M:%S'
    if inStr.find ('/') > 0:
        tmp_date_str = str(datetime.now().year)+'/'+inStr.split()[0]+' '+ inStr.split()[1]
        tmp_date_str = tmp_date_str.replace ('/', ' ')
        try:
            date = datetime.strptime (tmp_date_str, '%Y %d %m %H:%M:%S')
        except:
            return 0
        return time.mktime (date.timetuple())
    else:
        tmp_date_str = str(datetime.now().year)+' '+ str(datetime.now().day)+' '+str(datetime.now().month)+' '+ inStr.split()[0]+' '+ inStr.split()[1]
        try:
            date = datetime.strptime (tmp_date_str, '%Y %d %m %I:%M:%S %p')
        except:
            return 0
        return time.mktime (date.timetuple())

