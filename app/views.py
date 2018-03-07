from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, RoleEdit, AddGamerForm, ChatOptionsForm
from app.models import User, ROLE_USER, ROLE_ADMIN, Chat_opt, Chat
from app.user_managment import register_user, signin_user, users_list, edit_role
from app.gamers_managment import gamers_list, add_gamer_db
from app.telega_managment import telega_list, edit_chat_options, chat_list

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

@app.route('/users', methods = ['GET', 'POST'])
@login_required
def user_list():
    return render_template('users.html', users = users_list(), user = current_user)

@app.route('/roleedit/<id>', methods = ['GET','POST'])
@login_required
def update_user(id):
    if current_user.role !=2:
        return render_template("index.html",
                                title = 'Telega 2.0',
                                user = g.user)
    edited_user = User.query.filter_by(id=id).first()
    role = RoleEdit()
    if role.validate_on_submit():
        edit_role (edited_user.id, role.role.data)
        print (role.role.data)
    return render_template('role_edit.html', edited_user = edited_user, user = current_user, role = role)

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
    print ('-------------------------CHAT LIST---------------------')
    chatList = chat_list()
    for chat in chatList:
        print (chat)
    print ('-------------------------GAMERS LIST---------------------')
    print (telega_list(current_user.id))
    return render_template ('new_game.html', user = current_user)

@app.route ('/channels_active', methods =['GET'])
@login_required
def list_channels():
    tg_chats = Chat.query.all() 
    print (tg_chats)
    return render_template ('active_chats.html', user = current_user, tg_chats = tg_chats)

@app.route ('/chat_opt/<id>', methods =['GET', 'POST'])
@login_required
def chat_options(id):
    chat = Chat.query.filter_by(tg_id = id).first()
    chat_opt = Chat_opt.query.filter_by(chat = id).first()#[{'proxy':'true', 'multi_proxy':'false', 'bonuses':'true', 'bonuses_count':'13', 'codes':'false', 'codes_deny':'true', 'vote':'false', 'vote_percent':99}]
    chat_opt_frm = ChatOptionsForm()
    if request.method =='GET':
        chat_opt_frm.proxy.data = chat_opt.proxy
        chat_opt_frm.multi_proxy.data = chat_opt.multi_proxy
        chat_opt_frm.bonuses.data = chat_opt.bonuses
        chat_opt_frm.bonuses_count.data = chat_opt.bonuses_count
        chat_opt_frm.codes.data = chat_opt.codes
        chat_opt_frm.codes_deny.data = chat_opt.codes_deny
        chat_opt_frm.vote.data = chat_opt.vote
        chat_opt_frm.vote_percent.data = chat_opt.vote_percent 
    if request.method == 'POST':
            edit_chat_options (id,chat_opt_frm.proxy.data, chat_opt_frm.multi_proxy.data,
                                chat_opt_frm.bonuses.data, 
                                chat_opt_frm.bonuses_count.data,
                                chat_opt_frm.codes.data,
                                chat_opt_frm.codes_deny.data,
                                chat_opt_frm.vote.data,
                                chat_opt_frm.vote_percent.data)
            return redirect(url_for ('list_channels'))

    return render_template ('chat_options.html', user = current_user, chat=chat, chat_opt_frm=chat_opt_frm, chat_opt=chat_opt)
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
