from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    email: str


class CreateUserSchema(UserSchemaBase):
    password: str


class CreateSocialUserSchema(UserSchemaBase):
    pass  # 후에 전화번호, 성별 등 여러 정보 추가


class GetUserSchema(UserSchemaBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class SNSServiceInfoSchema(BaseModel):
    sns_service_id: str
