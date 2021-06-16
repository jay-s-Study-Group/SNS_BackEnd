from fastapi import APIRouter
from app.api.endpoints import users
from app.api.endpoints.sns import kakao
from app.api.endpoints import mentors

api_router = APIRouter()


api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(kakao.router, prefix="/sns", tags=["sns"])
api_router.include_router(mentors.router, prefix="/mentoring", tags=["mentoring"])