from bs4 import BeautifulSoup

left_panel_tag ='tdContentLeft'
header_tag = 'tableHeader'
right_panel_tag ='tdContentRight'
main_manu_tag = 'menuWrap'
info_block ='boxCenterContent'
vote_class ='enPnl1 border_rad2 clr2'
discuss_class ='discuss'
game_info_class =  'lnkGameTitle' #'boxGameInfo' 'yellow_darkgreen19'
game_info_table_class = 'gameInfo'
#test game gameengines/encounter/play/27833

def remove_login (page):
    soup = BeautifulSoup(page.text) 
    try:
        soup.find(id = left_panel_tag).replaceWith('')
        soup.find(id = header_tag).replaceWith('')
        soup.find(id = right_panel_tag).replaceWith('')
        soup.find(class_ = main_manu_tag).replaceWith('')
        soup.find(class_ = vote_class).replaceWith('')
        soup.find (id = info_block).replaceWith('')
        content = soup.prettify()
    except AttributeError:
        try:
            soup.find(class_ = discuss_class).replaceWith('')
            content = soup.prettify()
        except AttributeError:
            content = soup.prettify()
    return content
    
def game_info_list (page):
    soup = BeautifulSoup(page.text)
    content = ''
    for element in soup.findAll (id =game_info_class):
        #element.find (class_ =game_info_table_class) 
        content=content+element.prettify()+'<br>'
    return content
