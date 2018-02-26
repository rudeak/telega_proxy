from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, RoleEdit, AddGamerForm
from app.models import User, ROLE_USER, ROLE_ADMIN
from app.user_managment import register_user, signin_user, users_list
from app.gamers_managment import gamers_list, add_gamer_db
from app.telega_managment import telega_list

@lm.user_loader
def load_user(id):
     return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
 


@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template("index.html",
        title = 'Telega 2.0',
        user = g.user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    print (current_user)
    if g.user is not None and g.user.is_authenticated:
       return redirect(url_for('index'))
    print (g.user)
    form = LoginForm()
    if form.login.data != '' and form.login.data is not None:
            if signin_user (form.login.data, form.password.data):
                login_user(signin_user (form.login.data, form.password.data), True) 
                print(form.password.data)
                return redirect(url_for('index'))
            else:
                return render_template ('login.html', error = 'Невірний пароль', form = form)
    else:
            if form.new_password1.data !=form.new_password2.data:
                return render_template ('login.html', error = 'Паролі не співпадають', form = form)
            if form.new_password1 == '':
                return render_template ('login.html', error = 'Пароль порожній', form = form)
            if form.new_password1.data==form.new_password2.data and form.newlogin is not None:
               registration_result = register_user (form.newlogin.data, form.new_email.data, form.new_password1.data)
               if registration_result == 1:
                   return redirect(url_for('login'))
               else:
                   return render_template('login.html', error = registration_result, form = form)
            else:
               return render_template('login.html', form = form)
    return render_template('login.html', title = 'Увійти', form = form)

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(login = nickname).first()
    if user == None:
           flask.flash('User ' + nickname + ' not found.')
           return redirect(url_for('index'))
    return render_template('profile.html',
                            user = user)

@app.route('/users', methods = ['GET'])
@login_required
def user_list():
    form = RoleEdit()
    return render_template('users.html', users = users_list(), user = current_user, form = form)

@app.route('/users', methods = ['POST'])
@login_required
def update_user():
    form = RoleEdit()
    print ('role = ' +form.role.data+ ', id=' + form.user_id.data)
    print (request.form)
    return render_template('users.html', users = users_list(), user = current_user, form = form)

@app.route ('/gamers', methods = ['GET'])
@login_required
def list_gamers():
    form = RoleEdit()
    form_add = AddGamerForm()
    return render_template('gamers.html', gamers = gamers_list(g.user.id), user = current_user, form = form, add_gamer_frm = form_add)
    
@app.route ('/gamers', methods = ['POST'])
@login_required
def add_gamer():
    form = RoleEdit()
    form_add = AddGamerForm()
    if form_add.validate_on_submit():
        add_gamer_db(form_add.login.data, form_add.password.data, form_add.comment.data, g.user.id)
        form_add.login.data =''
        form_add.password.data =''
        form_add.comment.data =''
    return render_template('gamers.html', gamers = gamers_list(g.user.id), user = current_user, form = form, add_gamer_frm = form_add)

@app.route ('/telegram', methods = ['GET'])
@login_required
def list_telegram_users():
    form = RoleEdit()
    form_add = AddGamerForm()
    return render_template('telegram.html', tg_users = telega_list(g.user.id), user = current_user, form = form, add_gamer_frm = form_add)

@app.route ('/new_game', methods = ['GET'])
@login_required
def new_game_wizard():
    return render_template ('new_game.html', user = current_user)

@app.route ('/channels_active', methods =['GET'])
@login_required
def list_channels():
    tg_chats = ['tg_chat_id':'123', 'tg_chat_name':'test chat', 'tg_chat.tg_chat_avatar':g.user.avatar(32), 'tg_chat_game':'test game', 'id':'1053']
    return render_template ('active_chats.html', user = current_user, tg_chats = tg_chats)

#@app.before_request
#def before_request():
#    g.user = current_user

#@app.route('/logout')
#def logout():
#    logout_user()
#    return redirect(url_for('index'))

#@lm.user_loader
#def load_user(id):
#    return User.query.get(id)
