from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField, DecimalField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    login = TextField('login')
    password = TextField('password')
    newlogin = TextField('newlogin')
    new_email = TextField('new_email')
    new_password1 = TextField('new_password1')
    new_password2 = TextField('new_password2')
    isLogin = BooleanField('isLogin', default = True)
    isRegister = BooleanField('isRegister', default = True)

class RoleEdit(FlaskForm):
    role = SelectField('role',choices=[('0', 'Користувач'), ('1', 'Адміністратор'), ('2', 'Суперкористувач')], validators = [Required()])
   # user_id = TextField ('user_id', [Required()])

class AddGamerForm(FlaskForm):
    login = TextField('login', validators = [Required()])
    password = TextField('password', validators = [Required()])
    comment = TextField('comment', validators = [Required()])

class ChatOptionsForm (FlaskForm):
    proxy = BooleanField('proxy', validators= [Required()])
    multi_proxy = BooleanField('muli proxy', validators= [Required()])
    bonuses = BooleanField('bonuses', validators= [Required()])  
    bonuses_count = DecimalField ('bonuses count', validators=[Required()])
    codes = BooleanField('codes', validators= [Required()])
    codes_deny = BooleanField('codes deny', validators= [Required()])
    vote = BooleanField('vote', validators= [Required()])
    vote_percent = DecimalField('vote percent', validators= [Required()])

    




