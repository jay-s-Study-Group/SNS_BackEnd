from fastapi import APIRouter
from app.schemas import User, UserCreate
from app.crud import get_user_by_id, create_user

router = APIRouter()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    return get_user_by_id(user_id=user_id)


@router.post("/", response_model=User)
def create_user(user: UserCreate):
    return create_user(**user)
