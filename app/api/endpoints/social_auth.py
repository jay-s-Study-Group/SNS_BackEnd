from fastapi import APIRouter
from app.utils.authentication import (
    get_kakao_access_token,
)
from app.utils.config import load_config

SETTINGS = load_config()

router = APIRouter()


@router.get("/kakao/login_url")
def get_social_oauth_link_list():
    return {
        "login_url": "https://kauth.kakao.com/oauth/authorize?client_id={0}&response_type=code&redirect_uri={1}".format(
            SETTINGS.KAKAO_API_CLIENT_ID, SETTINGS.KAKAO_OAUTH_REDIRECT_URI
        )
    }


@router.get("/kakao/access-token")
def kakao_oauth_redirect(code: str):  # TODO: kakao login pydantic form 추가
    access_token = get_kakao_access_token(code)
    return {"access_token": access_token}
