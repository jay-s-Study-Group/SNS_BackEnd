import peewee
from .base import get_base_model

BaseModel = get_base_model()


class User(BaseModel):
    email = peewee.CharField(max_length=256, unique=True)
    password = peewee.CharField(max_length=256)
    is_active = peewee.BooleanField(default=False)
