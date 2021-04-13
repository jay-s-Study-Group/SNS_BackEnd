from app.models import User
from app.schemas import CreateUserSchema
from app.common.hashers import make_password
from app.databases.session import db


@db.db_connect
def create_user(user: CreateUserSchema):
    hashed_password = make_password(user.password)
    user_instance = User(email=user.email, password=hashed_password)
    user_instance.save()
    return user_instance


@db.db_connect
def get_user_by_id(user_id: int):
    user_instance = User.filter(User.id == user_id).first()
    return user_instance
