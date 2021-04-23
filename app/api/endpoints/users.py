from fastapi import APIRouter
from app.schemas import GetUserSchema, CreateUserSchema
from app.utils.hashers import make_password
from app.controllers.users import UserController

router = APIRouter()


@router.get("/{user_id}", response_model=GetUserSchema)
def get_user(user_id: int):
    return UserController().get_user_by_id(user_id)


@router.post("/", response_model=GetUserSchema)
def register(user: CreateUserSchema):
    user.password = make_password(user.password)
    return UserController().create_common_user(user.email, user.password)
