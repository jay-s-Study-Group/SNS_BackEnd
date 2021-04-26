from app.utils.hashers import make_password
from app.models.users import User


class UserController:
    def __init__(self):
        pass

    def create_common_user(self, email: str, password: str):
        hashed_password = make_password(password)
        user_instance = User(email=email, password=hashed_password)
        user_instance.save()
        return user_instance

    def get_user_by_id(self, user_id):
        user_instance = User.filter(User.id == user_id).first()
        return user_instance
