import hashlib
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import Gamers

def gamers_list (owner_id):
    return Gamers.query.filter_by(creator_id = owner_id)