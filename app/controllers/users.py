from typing import Tuple

from fastapi import HTTPException
from starlette import status
from app.core.utils.hashers import hash_password, check_password
from app.models.users import User, LocalAuthentication
from app.core.utils.token_handlers import jwt_payload_handler, jwt_encode_handler


class UserController:
    def __init__(self):
        pass

    def create_common_user(self, email: str, password: str) -> User:
        hashed_password = hash_password(password)
        user_instance = User.create(email=email)
        common_auth_instance = LocalAuthentication.create(
            user=user_instance.id, password=hashed_password
        )
        return user_instance

    def get_user_by_id(self, user_id: int) -> User:
        user_instance = User.filter(User.id == user_id).first()
        return user_instance

    def common_login(self, email: str, password: str) -> Tuple[User, str]:
        exist_user = User.filter(User.email == email).first()
        if not exist_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User instance could not find",
            )

        common_auth_instance = LocalAuthentication.filter(
            LocalAuthentication.user == exist_user.id
        ).first()
        if not common_auth_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LocalAuthentication instance could not find",
            )

        if not check_password(password, common_auth_instance.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The password is incorrect",
            )

        payload = jwt_payload_handler(exist_user)
        token = jwt_encode_handler(payload)

        return exist_user, token
