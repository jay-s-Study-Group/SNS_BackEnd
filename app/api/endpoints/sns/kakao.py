from fastapi import APIRouter, Response

from app.controllers.sns import KAKAOOAuthController
from core.config import load_config
from app.schemas.users import GetUserSchema
from app.schemas.sns import LoginURLSchema
from starlette import status

SETTINGS = load_config()

router = APIRouter()


@router.get("/kakao", response_model=LoginURLSchema, status_code=status.HTTP_200_OK)
def get_kakao_login_link():
    """
    사용자가 로그인 할 수 있는 kakao login page를 제공합니다.
    """
    login_url = KAKAOOAuthController().get_login_url()
    return {"login_url": login_url}


@router.get(
    "/kakao/callback", response_model=GetUserSchema, status_code=status.HTTP_200_OK
)
def callback_kakao(response: Response, code: str):
    """
    KAKAO 로그인의 Redirect URL 입니다.

    받은 code로 oauth_token을 발급 받고,
    유저가 회원가입 되어 있지 않다면 회원가입을 하고,
    계정이 연동되어 있지 않다면 계정 연동을 하고,
    로그인을 해 jwt 토큰과 유저 정보를 반환해 줍니다.
    """
    oauth_token = KAKAOOAuthController().get_oauth_token(code)
    user, token = KAKAOOAuthController().callback_process(oauth_token)
    response.headers["Authorization"] = "jwt " + token
    return user.__data__
