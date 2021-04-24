import requests
import jwt
from app.utils.config import load_config

CONFIG = load_config()


def jwt_encode_handler(payload):
    key = CONFIG.JWT_SECRET_KEY
    algorithm = CONFIG.JWT_ALGORITHM

    return jwt.encode(dict(payload), key, algorithm)


def jwt_decode_handler(token):
    key = CONFIG.JWT_SECRET_KEY
    algorithm = CONFIG.JWT_ALGORITHM
    return jwt.decode(token, key, algorithm)


def jwt_payload_handler(user):
    payload = {
        "sub": user.email,
        # "iss" : # TODO : 발급자 설정
        "email": user.email,
        # "exp": 1,  # TODO : 만료 시간 설정
        # "iat": 1,  # TODO : 발급 시간 설정
    }
    return payload


class BaseAuthentication:
    def authenticate(self, email, password):
        raise NotImplementedError("You must override authenticate method")


class JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # TODO : token 검증 후 user 인스턴스 반환
        return
