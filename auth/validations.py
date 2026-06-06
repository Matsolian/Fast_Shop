from auth import utils as auth_utils
from jwt.exceptions import InvalidTokenError

from auth.crud import oauth2_scheme, user_db
from auth.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from user.schemas import UserSchema


from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials


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


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} whrere expected {token_type!r}",
    )


def get_user_from_by_token_sub(payload: dict) -> UserSchema:
    usernname: str | None = payload.get("sub")
    if user := user_db.get(usernname):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid(user not found)",
    )


def get_current_auth_user(
    payload: HTTPAuthorizationCredentials = Depends(get_current_token_payload_user),
) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)


def get_auth_users_from_token_of_type(token_type: str):
    def get_auth_users_from_token(
        payload: dict = Depends(get_current_token_payload_user),
    ):
        validate_token_type(payload, token_type)
        return get_user_from_by_token_sub(payload)

    return get_auth_users_from_token


# class UserGetterFromToken:   # равнозначно get_auth_users_from_token_of_type, только без def in def
#     def __init__(self, token_type: str):
#         self.token_type = token_type

#     def __call__(
#         self,
#         payload: dict = Depends(get_current_token_payload_user),
#     ):
#         validate_token_type(payload, self.token_type)
#         return get_user_from_by_token_sub(payload)


def get_current_auth_user_for_refresh(
    payload: HTTPAuthorizationCredentials = Depends(get_current_token_payload_user),
) -> UserSchema:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
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


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_users_from_token_of_type(ACCESS_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
