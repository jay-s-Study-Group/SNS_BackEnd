from .users import *
from app.databases import db

db.create_tables([User, SocialAuth])
