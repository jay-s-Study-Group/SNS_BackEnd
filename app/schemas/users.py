from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    email: str


class CurrentUser(UserSchemaBase):
    id: int = None
    email: str = None
    is_active: bool = None


class CreateUserSchema(UserSchemaBase):
    password: str


class CreateSocialUserSchema(UserSchemaBase):
    pass  # 후에 전화번호, 성별 등 여러 정보 추가


class GetUserSchema(UserSchemaBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class SNSLoginSchema(BaseModel):
    oauth_token: str


class SNSServiceInfoSchema(BaseModel):
    sns_service_id: str
