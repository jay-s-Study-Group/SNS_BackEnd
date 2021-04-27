from pydantic import BaseModel


class LoginURLSchema(BaseModel):
    login_url: str
