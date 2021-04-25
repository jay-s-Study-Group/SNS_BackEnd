from fastapi import APIRouter, Depends, Header, Body, Response, Request
from fastapi.exceptions import HTTPException
from typing import Any
from app.controllers.sns import KAKAOOAuthController
from core.config import load_config
from app.schemas.users import GetUserSchema

SETTINGS = load_config()

router = APIRouter()


@router.get("/kakao/login-url", status_code=200)
def get_social_oauth_link_list():
    login_url = KAKAOOAuthController().get_login_url()
    return {"login_url": login_url}


@router.get("/kakao/oauth-token", status_code=200)
def kakao_oauth_redirect(code: str) -> Any:
    access_token = KAKAOOAuthController().get_oauth_token(code)
    return {"oauth_token": access_token}


def validate_oauth_token(oauth_token: str = Body(..., embed=True)):
    is_valid = KAKAOOAuthController().validate_oauth_token(oauth_token)

    if not is_valid:
        raise HTTPException(status_code=403, detail="oauth token is not valid")

    return oauth_token


@router.post("/kakao/connect", status_code=201)
def connect_user_to_kakao(
    request: Request,
    oauth_token=Depends(validate_oauth_token),
):
    social_auth_instance = KAKAOOAuthController().connect_social_login(
        oauth_token, request.user.id
    )
    return social_auth_instance.__data__


@router.post("/kakao/register", response_model=GetUserSchema, status_code=201)
def register_with_kakao(oauth_token=Depends(validate_oauth_token)):
    user_instance = KAKAOOAuthController().create_social_user(oauth_token)
    return user_instance.__data__


@router.post("/kakao/login", response_model=GetUserSchema, status_code=200)
def login_with_kakao(response: Response, oauth_token=Depends(validate_oauth_token)):
    user, token = KAKAOOAuthController().socical_login(oauth_token)
    response.headers["Authorization"] = "jwt " + token
    return user.__data__
