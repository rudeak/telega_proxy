from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    login = TextField('login')
    password = TextField('password')
    newlogin = TextField('newlogin')
    new_email = TextField('new_email')
    new_password1 = TextField('new_password1')
    new_password2 = TextField('new_password2')
    isLogin = BooleanField('isLogin', default = True)
    isRegister = BooleanField('isRegister', default = True)


