from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import Any
from app.utils.authentication import (
    jwt_decode_handler,
    get_kakao_access_token,
    jwt_payload_handler,
    jwt_encode_handler,
    get_kakao_user_info,
)
from app.utils.config import load_config
from app.crud.sns import (
    get_user_by_sns_service_id,
    create_social_user,
    create_social_auth,
)
from app.crud.users import get_user_by_email
from app.schemas.users import CreateSocialUserSchema, SNSLoginSchema

SETTINGS = load_config()

router = APIRouter()


@router.get("/kakao/login-url")
def get_social_oauth_link_list():
    return {
        "login_url": "https://kauth.kakao.com/oauth/authorize?client_id={0}&response_type=code&redirect_uri={1}".format(
            SETTINGS.KAKAO_API_CLIENT_ID, SETTINGS.KAKAO_OAUTH_REDIRECT_URI
        )
    }


@router.get("/kakao/oauth-token")
def kakao_oauth_redirect(code: str) -> Any:
    access_token = get_kakao_access_token(code)
    return {"oauth_token": access_token}


def get_current_user(authorization: str = Header(None)):
    if token := authorization.split()[0] not in ("jwt", "JWT"):
        raise HTTPException(status_code=400)
    decoded_payload = jwt_decode_handler(token)
    user_instance = get_user_by_email(decoded_payload["email"])
    return user_instance


def get_kakao_sns_service_id(login_info: SNSLoginSchema):
    oauth_token = login_info.oauth_token
    user_info = get_kakao_user_info(oauth_token)
    return user_info["id"]


@router.post("/kakao/connect")
def connect_user_to_kakao(
    user=Depends(get_current_user),
    sns_service_id=Depends(get_kakao_sns_service_id),
):
    social_auth_instance = create_social_auth(
        platform="kakao", sns_service_id=sns_service_id, user=user
    )
    # TODO 중복 계정 체크 추가
    social_auth_instance.save()

    return social_auth_instance


@router.post("/kakao/register")
def register_with_kakao(
    user: CreateSocialUserSchema, sns_service_id=Depends(get_kakao_sns_service_id)
):
    user_instance = create_social_user(
        user=user, sns_service_id=sns_service_id, platform="kakao"
    )
    # TODO 중복 계정 체크 추가
    return user_instance


@router.post("/kakao/login")
def login_with_kakao(sns_service_id=Depends(get_kakao_sns_service_id)):
    user_instance = get_user_by_sns_service_id(sns_service_id)
    if user_instance is None:
        raise HTTPException(status_code=404, detail="Could not find user instance")

    payload = jwt_payload_handler(user_instance)
    token = jwt_encode_handler(payload)
    headers = {"Authorization": "jwt " + token}
    return JSONResponse(headers=headers)
