import jwt
from app.core.config import load_config

CONFIG = load_config()


def jwt_encode_handler(payload):
    key = CONFIG.JWT_SECRET_KEY
    algorithm = CONFIG.JWT_ALGORITHM

    return jwt.encode(dict(payload), key, algorithm)


def jwt_decode_handler(token: str):
    token = token.encode()
    key = CONFIG.JWT_SECRET_KEY
    algorithm = CONFIG.JWT_ALGORITHM
    decoded = jwt.decode(token, key, algorithm)
    return decoded


def jwt_payload_handler(user):
    payload = {
        "sub": user.email,
        # "iss" : # TODO : 발급자 설정
        "email": user.email,
        "id": user.id,
        # "exp": 1,  # TODO : 만료 시간 설정
        # "iat": 1,  # TODO : 발급 시간 설정
    }
    return payload
