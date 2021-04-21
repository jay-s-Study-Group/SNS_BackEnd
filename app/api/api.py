from fastapi import APIRouter
from .endpoints import users
from .endpoints.sns import kakao

api_router = APIRouter()


api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(kakao.router, prefix="/sns", tags=["sns"])
