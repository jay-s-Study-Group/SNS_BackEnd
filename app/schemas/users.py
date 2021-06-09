from pydantic import BaseModel
from typing import List


class UserSchemaBase(BaseModel):
    email: str


class CurrentUser(UserSchemaBase):
    id: int = None
    email: str = None
    is_active: bool = None


class CreateUserSchema(UserSchemaBase):
    password: str


class UpdateUserSchema(UserSchemaBase):
    name: str
    mentoring_fields: List[str]
    self_introduction: str
    phone_number: str
    profile_url: str


class GetUserSchema(UserSchemaBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class LocalLoginSchema(BaseModel):
    email: str
    password: str
