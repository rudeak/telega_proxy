import requests
import random
from flask import Flask, request

app = Flask(__name__)

login = 'rudeak'
password = 'cvtnfyf1'
domain = 'lutsk.quest.ua'
answers = ['ап']
id = random.randrange(11111111, 99999999)
print ('id ='+str(id))
#ddlNetwork	2
#EnButton1	Вход
#Login	rudeak
#Password	cvtnfyf1
#socialAssign	0

print(domain)
r = requests.Session()
def login_engine(domain_in, login_in, password_in):
    page= r.post('http://'+domain_in+'/login.aspx?', data={'Login': login_in, 'Password' : password_in} )
    return page.text

@app.route('/')
def home():
    print ('home')
    return r.get('http://'+domain).text 

@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    url = "http://%s/%s?%s&lol=%s" % (domain, path, request.query_string, random.random())
    print ('new url ='+url)
    print ('path ='+path)
    if request.method == 'GET':
        page = r.get(url)
    return page.text
    if request.method == 'POST':
        post_data = {}
        for k, v in request.form.to_dict().items():
            post_data[k] = v.encode('utf-8')
            if k == 'Answer':
                answer = post_data[k]
        if answer in answers:
            page = dl.download(url)
            if answer == 'ап':
                global answers
                answers = ['ап']
        else:
            answers.append(answer)
            page = r.post (url, post_data)
            return page.text



if __name__ == '__main__':
    login_engine(domain, login, password)
    app.run(host= '0.0.0.0', debug = True)
