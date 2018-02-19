from flask import render_template, flash, redirect
from flask_login import login_required
from app import app, db, lm
from app.forms import LoginForm
from app.models import User, ROLE_USER, ROLE_ADMIN



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = { 'nickname': 'Miguel' } # выдуманный пользователь
    return render_template("index.html",
        title = 'Home',
        user = user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    print (form.login.data)
    if form.login.data != '' and form.login.data is not None:
            print(form.password.data)
            return render_template("index.html")
    else:
            if form.new_password1.data==form.new_password2.data and form.newlogin is not None:
               print('registration!!!')
            else:
               return render_template('login.html', title = 'passwords not equal', form = form)
    return render_template('login.html', title = 'Sign In', form = form)

