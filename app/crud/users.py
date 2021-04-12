from app.models import User
from app.schemas import UserCreate
from app.common.hashers import make_password
from app.databases.session import db


@db.db_connect
def create_user(user: UserCreate):
    hashed_password = make_password(user.password)
    user_instance = User(email=user.email, password=hashed_password)
    user_instance.save()
    return user_instance


@db.db_connect
def get_user_by_id(user_id: int):
    return User.filter(User.id == user_id).first()
