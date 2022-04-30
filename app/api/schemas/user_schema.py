from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from app.services.enums import UserRole


class UserSchema(BaseModel):
    role: UserRole = None
    name: Optional[constr(max_length=255)] = None
    email: Optional[EmailStr]
    username: constr(max_length=50)
    date_joined: datetime = None
    last_seen: Optional[datetime] = None
    disabled: Optional[bool] = None


class UserInDB(UserSchema):
    hashed_password: constr(max_length=255)
