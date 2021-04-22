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


def get_kakao_access_token(code):  # TODO : core 부분으로 분리
    data = {
        "grant_type": "authorization_code",
        "client_id": CONFIG.KAKAO_API_CLIENT_ID,
        "redirect_uri": CONFIG.KAKAO_OAUTH_REDIRECT_URI,
        "code": code,
    }
    response = requests.post("https://kauth.kakao.com/oauth/token", data=data)
    if response.status_code in (400, 401):
        raise Exception(response.text)  # TODO: 직접 만든 exception 모듈로 교체
    token_info = response.json()
    access_token = token_info["access_token"]
    return access_token


def get_kakao_user_info(oauth_token):  # TODO: status가 200이 아닐 경우 에러 핸들링
    headers = {"Authorization": "Bearer " + oauth_token}
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)

    return response.json()


class BaseAuthentication:
    def authenticate(self, email, password):
        raise NotImplementedError()  # TODO: Add  error message


class JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # TODO : token 검증 후 user 인스턴스 반환
        return
