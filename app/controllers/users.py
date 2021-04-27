from fastapi import HTTPException
from starlette import status
from core.utils.hashers import hash_password
from app.models.users import User, LocalAuthentication
from core.utils.token_handlers import jwt_payload_handler, jwt_encode_handler


class UserController:
    def __init__(self):
        pass

    def create_common_user(self, email: str, password: str):
        hashed_password = hash_password(password)
        user_instance = User(email=email, password=hashed_password)
        user_instance.save()
        return user_instance

    def get_user_by_id(self, user_id):
        user_instance = User.filter(User.id == user_id).first()
        return user_instance

    def local_login(self, email, password):
        exist_user = User.filter(User.email == email).first()
        if not exist_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User instance could not find",
            )

        hashed_password = hash_password(password)
        local_auth_instance = LocalAuthentication.filter(
            LocalAuthentication.user == exist_user.id,
            LocalAuthentication.password == hashed_password,
        ).first()
        if not local_auth_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LocalAuthentication instance could not find",
            )

        payload = jwt_payload_handler(exist_user)
        token = jwt_encode_handler(payload)

        return exist_user, token
