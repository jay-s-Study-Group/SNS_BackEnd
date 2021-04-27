from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    email: str


class CurrentUser(UserSchemaBase):
    id: int = None
    email: str = None
    is_active: bool = None


class CreateUserSchema(UserSchemaBase):
    password: str


class GetUserSchema(UserSchemaBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class LocalLoginSchema(BaseModel):
    email: str
    password: str
