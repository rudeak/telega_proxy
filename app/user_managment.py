import hashlib
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import User

def register_user (nickname, email1, password1):
    if password1 is None:
                return ('Пароль порожній')
    password_hash = hashlib.sha256(password1.encode()).hexdigest()
    new_user = User(nickname, email1, password_hash,0)
    if User.query.filter_by (login = nickname).count() >0:
        return ('Користувач з таким логіном існує')
    if User.query.filter_by (email = email1).count () > 0:
        return ('Користувач з таким е-мейлом існує')
    db.session.add(new_user)
    try:
        db.session.commit()
        user = User.query.filter_by(login = nickname).first()
        if user.id == 1:
            user.role = 2
            db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'Помилка звернення до бази даних'

def signin_user (nickname, password1):
    password_hash = hashlib.sha256(password1.encode()).hexdigest()
    if User.query.filter_by (login = nickname) == 0
        return 0
    user = User.query.filter_by (login = nickname).first()
    if password_hash == user.password:
        return user
    else:
        return False

def users_list():
    users = User.query.all()
    return users

def edit_role (id, role):
    user = User.query.filter_by (id=id).first()
    user.role = role
    if id == 1:
       user.role = 2 
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'Помилка звернення до бази даних'

