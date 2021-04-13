from fastapi import APIRouter
from app.schemas import GetUserSchema, CreateUserSchema
from app.crud import get_user_by_id, create_user

router = APIRouter()


@router.get("/{user_id}", response_model=GetUserSchema)
def get_user(user_id: int):
    user_instance = get_user_by_id(user_id=user_id)
    return user_instance


@router.post("/", response_model=GetUserSchema)
def register(user: CreateUserSchema):
    return create_user(user)
