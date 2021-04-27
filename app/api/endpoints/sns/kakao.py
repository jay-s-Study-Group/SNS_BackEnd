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


@router.get("/kakao/callback", response_model=GetUserSchema, status_code=200)
def callback_kakao(response: Response, code: str):
    oauth_token = KAKAOOAuthController().get_oauth_token(code)
    user, token = KAKAOOAuthController().callback_process(oauth_token)
    response.headers["Authorization"] = "jwt " + token
    return user.__data__
