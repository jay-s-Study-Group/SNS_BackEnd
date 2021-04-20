import requests
from app.utils.config import load_config

CONFIG = load_config()


def get_kakao_access_token(code):
    data = {
        "grant_type": "authorization_code",
        "client_id": CONFIG.KAKAO_API_CLIENT_ID,
        "redirect_uri": CONFIG.KAKAO_OAUTH_REDIRECT_URI,
        "code": code,
    }
    response = requests.post("https://kauth.kakao.com/oauth/token", data=data)
    print(response.status_code)
    if response.status_code in (400, 401):
        raise Exception(response.text)  # TODO: 직접 만든 exception 모듈로 교체
    token_info = response.json()
    access_token = token_info["access_token"]
    return access_token


def get_kakao_user_info(access_token):
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)

    return response.json()
