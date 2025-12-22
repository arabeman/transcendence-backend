from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
