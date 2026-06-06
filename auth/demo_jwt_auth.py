from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel

from auth.helpers import (
    create_access_token,
    create_refresh_token,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
)
from user.schemas import UserSchema
from auth import utils as auth_utils


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/JWT/jwt/login",  # вставляем путь для нашей  авторизации
)

router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


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


def get_current_token_payload_user(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),  # для brearer
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}",  # ООООООООЧень плохая праткика показывать юх
        )


def get_current_auth_user(
    payload: HTTPAuthorizationCredentials = Depends(get_current_token_payload_user),
) -> UserSchema:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {token_type!r} whrere expected {ACCESS_TOKEN_TYPE!r}",
        )
    usernname: str | None = payload.get("sub")
    if user := user_db.get(usernname):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid(user not found)",
    )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


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
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        # token_type="Bearer",  # можно убрать, я же добавил в классе TokenInfo обработку
    )


@router.post("/refresh/", response_model=TokenInfo)
def auth_refresh_jwt():
    pass


@router.get("/username/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload_user),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
