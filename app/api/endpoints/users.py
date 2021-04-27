from fastapi import APIRouter, Response
from app.schemas import GetUserSchema, CreateUserSchema, LocalLoginSchema
from app.controllers.users import UserController
from starlette import status

router = APIRouter()


@router.get("/{user_id}", response_model=GetUserSchema, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    return UserController().get_user_by_id(user_id)


@router.post(
    "/register", response_model=GetUserSchema, status_code=status.HTTP_201_CREATED
)
def register(user: CreateUserSchema):
    """
    email, password로 유저를 생성합니다.
    - **email** : user email (should be unique)
    - **password** : user password (must be at least 8 letters long)
    """
    return UserController().create_common_user(user.email, user.password)


@router.post("/login", response_model=GetUserSchema, status_code=status.HTTP_200_OK)
def register(response: Response, user: LocalLoginSchema):
    """
    email, password로 로그인을 진행합니다.
    - **email** : user email (should be unique)
    - **password** : user password (must be at least 8 letters long)
    """
    user, token = UserController().local_login(user.email, user.password)
    response.headers["Authorization"] = "jwt " + token
    return user.__data__
