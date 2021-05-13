from fastapi import APIRouter
from app.endpoints import users
from app.endpoints.sns import kakao

api_router = APIRouter()


api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(kakao.router, prefix="/sns", tags=["sns"])
