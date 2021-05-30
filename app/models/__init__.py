from .users import *
from app.core.databases import db

db.create_tables([User, LocalAuthentication, SocialAuthentication])
