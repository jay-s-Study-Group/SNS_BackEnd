import requests
from app.common.util import conf

SETTINGS = conf()


class BaseSocialAuthentication:
    def get_access_token(self, code):
        raise NotImplementedError()  # TODO: Add error message


class KakaoSocialAuthentication(BaseSocialAuthentication):
    def __init__(self):
        self.redirect_uri = conf().KAKAO_OAUTH_REDIRECT_URI

    def get_access_token(self, code):
        data = {
            "grant_type": "authorization_code",
            "client_id": SETTINGS.KAKAO_API_CLIENT_ID,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        response = requests.post("https://kauth.kakao.com/oauth/token", data=data)
        print(response.status_code)
        if response.status_code in (400, 401):
            raise Exception(response.text)  # TODO: 직접 만든 exception 모듈로 교체
        token_info = response.json()
        access_token = token_info["access_token"]
        return access_token
