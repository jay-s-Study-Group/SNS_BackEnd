from fastapi import APIRouter
from .endpoints import users, social_auth

api_router = APIRouter()


api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    social_auth.router, prefix="/social-auth", tags=["social-auth"]
)
