from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str | None = None
    

    model_config = ConfigDict(from_attributes=True)
