
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from app import db

db.create_all()
