from fastapi import APIRouter
from app.schemas import User
from app.crud import get_user_by_id

router = APIRouter()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    return get_user_by_id(user_id=user_id)
