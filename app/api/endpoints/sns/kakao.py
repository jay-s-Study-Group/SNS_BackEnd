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
    `ENG subscribe: Redirect the Kakao login page where users can log in.` \n
    `KOR subscribe: 사용자가 로그인 할 수 있는 kakao login page를 제공합니다.`
    """
    login_url = KAKAOOAuthController().get_login_url()
    return {"login_url": login_url}


@router.get(
    "/kakao/callback", response_model=GetUserSchema, status_code=status.HTTP_200_OK
)
def callback_kakao(response: Response, code: str):
    """
    `ENG subscribe: After receiving the code and
                   registering the user or linking the account,
                   log in and return the token and user information.`\n
    `KOR subscribe: KAKAO 로그인의 Redirect URL 입니다.
                    받은 code로 회원가입 또는 계정
                    연동을 진행한 뒤 로그인하여 jwt
                    토큰과 유저 정보를 반환합니다.` \n
    param:
    ### url (query)
    code : str = kakao code
    """
    oauth_token = KAKAOOAuthController().get_oauth_token(code)
    user, token = KAKAOOAuthController().callback_process(oauth_token)
    response.headers["Authorization"] = "jwt " + token
    return user.__data__
