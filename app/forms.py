from flaskform import Form
from wtforms import TextField, BooleanField, SelectField
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

class RoleEdit(Form):
    role = SelectField('role',choices=[('0', 'Користувач'), ('1', 'Адміністратор'), ('2', 'Суперкористувач')])
    user_id = TextField ('user_id', [Required()])




