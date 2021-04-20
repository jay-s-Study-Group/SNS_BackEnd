from fastapi import APIRouter
from app.utils.authentication import KakaoSocialAuthentication
from app.utils.config import load_config

SETTINGS = load_config()

router = APIRouter()


@router.get("/login")
def get_social_oauth_link_list():
    return {
        "kakao_login": "https://kauth.kakao.com/oauth/authorize?client_id={0}&response_type=code&redirect_uri={1}".format(
            SETTINGS.KAKAO_API_CLIENT_ID, SETTINGS.KAKAO_OAUTH_REDIRECT_URI
        )
    }


@router.get("/kakao-login")
def kakao_oauth_redirect(code: str):  # TODO: kakao login pydantic form 추가
    authentication = KakaoSocialAuthentication()
    access_token = authentication.get_access_token(code)
    return {"access_token": access_token}
