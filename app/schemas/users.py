from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    email: str


class CreateUserSchema(UserSchemaBase):
    password: str


class GetUserSchema(UserSchemaBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
