#test git
import requests
import random
from flask import Flask, request, jsonify
from parser import remove_login, game_info_list
from game_list import get_game_list

app = Flask(__name__)

login = 'rudeak'
password = 'fkmnfdbcnf'
domain = 'demo.en.cx'
answers = ['up']
#id = str(random.randrange(11111111, 99999999))
id = str (1)
print ('id ='+id)
#ddlNetwork	2
#EnButton1	Вход
#Login	rudeak
#Password	cvtnfyf1
#socialAssign	0

print(domain)
r = requests.Session()
def login_engine(domain_in, login_in, password_in):
    page= r.post('http://'+domain_in+'/login.aspx?', data={'Login': login_in, 'Password' : password_in} )
    parsed_page = remove_login (page)
    return parsed_page

@app.route('/')
def login_settings():
    return 'login page'

@app.route('/proxy/'+id+'/')
def home():
    print ('home')
    page = r.get('http://'+domain)
    parsed_page = remove_login (page)
    return parsed_page
    

@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    url = "http://%s/%s?%s" % (domain, path, request.query_string.decode("utf-8") )
    if request.method == 'GET':
        page = r.get(url)
        parsed_page = remove_login (page)
        return parsed_page
        #return page.text
    if request.method == 'POST':
        post_data = {}
        for k, v in request.form.to_dict().items():
            post_data[k] = v.encode('utf-8')
            if k == 'LevelAction.Answer':
                answer = post_data[k]
                #return v.encode('utf-8')
               
        if answer in answers:
            page = r.get(url)
            if answer.decode("utf-8")  == 'up':
                print (answer.decode("utf-8"))
                answers.clear()
        else:
            answers.append(answer)
            page = r.post (url, post_data)
        return page.text

@app.route ('/'+id+'/games')
def list():
    page = r.get('http://'+domain) 
    return game_info_list (page)

@app.route ('/api/games', methods=['GET'])
def api_games():
    page = r.get('http://'+domain) 
    return jsonify({'href':game_info_list (page)})

@app.route ('/api/domain', methods=['GET'])
def api_domain():
    return jsonify({'domain':domain})

@app.route ('/api/login', methods=['GET'])
def api_login():
    return jsonify({'login':login, 'pass':password})

@app.route ('/api/domain', methods=['POST'])
def api_setdomain():
    if not request.json or not 'domain' in request.json:
        return jsonify ({'error':'error domain setting'})
    else:
        print (request.json['domain'])
        domain = request.json['domain']
        print ('new domain=' + domain )
    return jsonify({'domain':domain})



if __name__ == '__main__':
    login_engine(domain, login, password)
    app.run(host= '0.0.0.0', debug = True)
