from .users import *
from core.databases import db

db.create_tables([User, SocialAuth])
