from fastapi import APIRouter
from app.schemas import GetUserSchema, CreateUserSchema
from core.utils.hashers import hash_password
from app.controllers.users import UserController

router = APIRouter()


@router.get("/{user_id}", response_model=GetUserSchema)
def get_user(user_id: int):
    return UserController().get_user_by_id(user_id)


@router.post("/register", response_model=GetUserSchema)
def register(user: CreateUserSchema):
    """
    email, password로 유저를 생성합니다.
    - **email** : user email (should be unique)
    - **password** : user password (must be at least 8 letters long)
    """
    return UserController().create_common_user(user.email, user.password)
