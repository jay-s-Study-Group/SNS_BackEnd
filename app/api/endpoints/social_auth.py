from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.utils.authentication import (
    get_kakao_user_info,
    get_kakao_access_token,
    jwt_payload_handler,
    jwt_encode_handler,
)
from app.utils.config import load_config
from app.crud.sns import get_user_by_sns_service_id

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


def get_current_user(token: str):  # TODO
    pass


def get_kakao_user_info(access_token: str):  # TODO
    pass


@router.get("/kakao/connect")
def connect_user_to_kakao(  # TODO
    user=Depends(get_current_user), sns_user=Depends(get_kakao_user_info)
):
    # TODO : SocialAuth를 user id, platform, sns_service_id 와 함께 생성
    return


@router.get("/kakao/login")
def login_with_kakao(sns_service_id: str):  # TODO
    user_instance = get_user_by_sns_service_id(sns_service_id)

    payload = jwt_payload_handler(user_instance)
    token = jwt_encode_handler(payload)
    headers = {"Authorization": "jwt " + token}
    return JSONResponse(headers=headers)
