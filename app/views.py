from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm
from app.models import User, ROLE_USER, ROLE_ADMIN
from app.user_managment import register_user, signin_user, users_list

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
