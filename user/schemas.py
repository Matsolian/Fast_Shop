from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr
from annotated_types import MinLen, MaxLen


class Create_User(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    emaIL: EmailStr


class UserShema(BaseModel):
    model_config = ConfigDict(
        strict=True
    )  # чтобы была строгая типизация и  не перетакили типы из друг в друга
    username: str
    passwd: bytes
    email: str | None = None
    active: bool = True
