from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from pydantic import BaseModel

from user.schemas import UserSchema
from auth import utils as auth_utils

router = APIRouter(prefix="/jwt", tags=["JWT"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


John = UserSchema(
    username="john",
    passwd=auth_utils.hash_passwd("qwerty"),
    email="example@lol.com",
    active=True,
)

Sam = UserSchema(
    username="Sam",
    passwd=auth_utils.hash_passwd("qwerty"),
    email="example@uoi.com",
    active=True,
)


user_db: dict[str, UserSchema] = {
    John.username: John,
    Sam.username: Sam,
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid login or password",
    )
    if not (user := user_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_passwd(
        password=password,
        hashed_password=user.passwd,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive",
        )
    return user


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,  # объект о чем речь, обычно это ууникальный id, но для примера и имя сойдет пока что
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )

