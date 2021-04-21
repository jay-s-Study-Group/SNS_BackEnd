from app.models import User
from app.schemas import CreateUserSchema
from app.utils.hashers import make_password
from app.databases.session import db


@db.db_connect
def create_user(user: CreateUserSchema):
    user_instance = User(email=user.email, password=user.password)
    user_instance.save()
    return user_instance


@db.db_connect
def get_user_by_id(user_id: int):
    user_instance = User.filter(User.id == user_id).first()
    return user_instance


@db.db_connect
def get_user_by_email(email: str):
    user_instance = User.filter(User.email == email).first()
    return user_instance
