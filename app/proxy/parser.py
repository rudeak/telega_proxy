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

def get_game_info(page):
    soup = BeautifulSoup(page.text)
    content =soup.a(id = game_name_id)
    print (content)
    return content