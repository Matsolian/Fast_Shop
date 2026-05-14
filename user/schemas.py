from typing import Annotated
from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen


class Create_User(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    emaIL: EmailStr
