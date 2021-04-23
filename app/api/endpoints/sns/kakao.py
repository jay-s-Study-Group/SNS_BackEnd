from fastapi import APIRouter, Depends, Header, Body
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import Any
from app.utils.authentication import (
    jwt_decode_handler,
)
from app.controllers.sns import KAKAOOAuthController
from app.utils.config import load_config
from app.models.users import User

SETTINGS = load_config()

router = APIRouter()


@router.get("/kakao/login-url")
def get_social_oauth_link_list():
    login_url = KAKAOOAuthController().get_login_url()
    return JSONResponse(content={"login_url": login_url}, status_code=200)


@router.get("/kakao/oauth-token")
def kakao_oauth_redirect(code: str) -> Any:
    access_token = KAKAOOAuthController().get_oauth_token(code)
    return JSONResponse(content={"oauth_token": access_token}, status_code=200)


def get_current_user(authorization: str = Header(None)):
    if token := authorization.split()[0] not in ("jwt", "JWT"):
        raise HTTPException(status_code=403)
    decoded_payload = jwt_decode_handler(token)
    user_instance = User.filter(User.email == decoded_payload["email"]).first()
    return user_instance


def validate_oauth_token(oauth_token: str = Body(..., embed=True)):
    is_valid = KAKAOOAuthController().validate_oauth_token(oauth_token)

    if not is_valid:
        raise HTTPException(status_code=403, detail="oauth token is not valid")

    return oauth_token


@router.post("/kakao/connect")
def connect_user_to_kakao(
    user=Depends(get_current_user),
    oauth_token=Depends(validate_oauth_token),
):
    social_auth_instance = KAKAOOAuthController().connect_social_login(
        oauth_token, user
    )
    return JSONResponse(content=social_auth_instance.__data__, status_code=200)


@router.post("/kakao/register")
def register_with_kakao(oauth_token=Depends(validate_oauth_token)):
    user_instance = KAKAOOAuthController().create_social_user(oauth_token)
    return JSONResponse(content=user_instance.__data__, status_code=201)


@router.post("/kakao/login")
def login_with_kakao(oauth_token=Depends(validate_oauth_token)):
    user, token = KAKAOOAuthController().socical_login(oauth_token)
    headers = {"Authorization": "jwt " + token}
    return JSONResponse(content=user.__data__, headers=headers, status_code=200)
