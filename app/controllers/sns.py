import requests
from fastapi import HTTPException

from app.utils.config import load_config
from app.models.users import SocialAuth, User
from utils.authentication import jwt_payload_handler, jwt_encode_handler

CONFIG = load_config()


class KAKAOOAuthController:
    platform = "kakao"

    def get_login_url(self):
        return "https://kauth.kakao.com/oauth/authorize?client_id={0}&response_type=code&redirect_uri={1}".format(
            CONFIG.KAKAO_API_CLIENT_ID, CONFIG.KAKAO_OAUTH_REDIRECT_URI
        )

    def get_oauth_token(self, code):
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

    def connect_social_login(self, oauth_token: str, user: User):
        kakao_user_info = self._get_kakao_user_info(oauth_token)
        sns_service_id = kakao_user_info["id"]

        social_auth_instance = SocialAuth(
            platform="kakao", sns_service_id=sns_service_id, user=user
        )
        social_auth_instance.save()
        return social_auth_instance

    def validate_oauth_token(self, oauth_token: str) -> bool:
        headers = {"Authorization": "Bearer " + oauth_token}
        response = requests.get(
            "https://kapi.kakao.com/v1/user/access_token_info", headers=headers
        )
        if response.status_code == 200:
            return True

        return False

    def create_social_user(self, oauth_token: str):
        kakao_user_info = self._get_kakao_user_info(oauth_token)
        sns_service_id = kakao_user_info["id"]
        credentials = {"email": kakao_user_info["kakao_account"]["email"]}
        exist_user = User.filter(User.email == credentials["email"])

        if exist_user:
            raise HTTPException(status_code=400, detail="User instance already exists")

        user_instance = User.create(**credentials)
        social_auth_instance = SocialAuth.create(
            user=user_instance.id, sns_service_id=sns_service_id, platform=self.platform
        )
        return user_instance

    def socical_login(self, oauth_token):
        kakao_user_info = self._get_kakao_user_info(oauth_token)
        sns_service_id = kakao_user_info["id"]
        social_auth_instance = SocialAuth.filter(
            SocialAuth.sns_service_id == sns_service_id
        ).first()
        if social_auth_instance is None:
            raise HTTPException(
                status_code=404, detail="Could not find SocialAuth instance"
            )
        user_instance = User.filter(User.id == social_auth_instance.user).first()
        if user_instance is None:
            raise HTTPException(status_code=404, detail="Could not find user instance")
        payload = jwt_payload_handler(user_instance)
        token = jwt_encode_handler(payload)

        return user_instance, token

    def _get_kakao_user_info(self, oauth_token):  # TODO: status가 200이 아닐 경우 에러 핸들링
        headers = {"Authorization": "Bearer " + oauth_token}
        response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)

        return response.json()
