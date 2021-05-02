import jwt

from typing import Tuple, Optional

from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from schemas.users import CurrentUser
from core.utils.token_handlers import jwt_decode_handler


class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user
        try:
            token_type, token = authorization.split(" ")
            if token_type.lower() not in ("jwt",):
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = jwt_decode_handler(token)
            user_id = payload.get("id")
            user_email = payload.get("email")
            user_is_active = payload.get("is_active")
        except jwt.PyJWTError:
            return False, current_user

        current_user.id = user_id
        current_user.email = user_email
        current_user.is_active = user_is_active
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
