from auth import utils as auth_utils
from jwt.exceptions import InvalidTokenError

from auth.crud import oauth2_scheme, user_db
from auth.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from user.schemas import UserSchema


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials


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

def validate_token_type(payload:dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {token_type!r} whrere expected {TOKEN_TYPE_FIELD!r}",
        )


def get_current_auth_user(
    payload: HTTPAuthorizationCredentials = Depends(get_current_token_payload_user),
) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
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
