from fastapi import APIRouter, Response
from app.schemas import (
    GetUserSchema,
    CreateUserSchema,
    LocalLoginSchema,
    UpdateUserSchema,
)
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
    `ENG subscribe: Create user with email and password.` \n
    `KOR subscribe: email, password로 유저를 생성합니다.`
    ### body (json)
    - **email** : str = user email (should be unique)
    - **password** : str = user password (must be at least 8 letters long)
    """
    return UserController().create_common_user(user.email, user.password)


@router.post("/login", response_model=GetUserSchema, status_code=status.HTTP_200_OK)
def common_login(response: Response, user: LocalLoginSchema):
    """
    `ENG subscribe: Log in with email and password.` \n
    `KOR subscribe: email, password로 로그인을 진행합니다.`
    ### body (json)
    - **email** : str = user email (should be unique)
    - **password** : str = user password (must be at least 8 letters long)
    """
    user, token = UserController().common_login(user.email, user.password)
    response.headers["Authorization"] = "jwt " + token
    return user.__data__


@router.patch(
    "/{user_id}", response_model=GetUserSchema, status_code=status.HTTP_200_OK
)
def update_user_info(response: Response, user_id: int, user: UpdateUserSchema):
    """
    `ENG subscribe: Update user data with user_id, body.` \n
    `KOR subscribe: user_id에 맞는 유저의 정보를 body의 값으로 변경합니다.`
    ### body (json)
    - **email** : str = user email (should be unique)
    - **password** : str = user password (must be at least 8 letters long)
    - **name** : str = user name
    - **mentoring_fields** : List[str] = user mentoring fields
    - **self_introduction** : str = user self introduction
    - **phone_number** : str = user phone number
    - **profile_url** : str = user profile s3 url
    """
    additional_data = dict(user)
    user = UserController().update_user(user_id=user_id, **additional_data)
    return user.__data__
