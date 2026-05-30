import secrets
import time
from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, Header, status, Response, Cookie

from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo_auth", tags=["Demo Authh"])
security = HTTPBasic()


@router.get("/basic-auth/")  # Выводит подчистую твой юзернейм и пароль
def demo_basic_credantials(
    credantials: Annotated[
        HTTPBasicCredentials,
        Depends(security),
    ],
):

    return {
        "message": "hello",
        "username": credantials.username,
        "password": credantials.password,
    }


usernames_to_password = {  # Так никогда не храним, это простой пример
    "admin": "admin",
    "admin1": "admin12",
    "admin2": "admin23",
}

static_auth_token_to_username = {  # Так никогда не храним, это простой пример
    "brgfvedc": "admin",
    "trwfgedwggyht6uj": "admin12",
    "i7ujn6yh4bg5t3vrfecii7uh6": "admin23",
}


def get_auth_user_username(  # Проверка с админами
    credantials: Annotated[
        HTTPBasicCredentials,
        Depends(security),
    ],
):
    unauted_exc = HTTPException(  # Наша кастомная ошибка
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_password.get(credantials.username)

    if credantials.username not in usernames_to_password:
        raise unauted_exc

    # secrets  Могут по времени сравнения вычислить пароль, поэтому делай через secret
    if not secrets.compare_digest(
        credantials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauted_exc

    return credantials.username


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-secret-auth-token"),
) -> str:

    if username := static_auth_token_to_username.get(
        static_token
    ):  # тут мы прсото смотрим есть ли значение и сразу выдаем
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    )

    # if static_token not in static_auth_token_to_username:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    #     )
    # return static_auth_token_to_username[static_token]  # тут мы еще проверку делаем


@router.get("/basic-auth_username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):

    return {
        "message": "hello",
        "username": auth_username,
    }


@router.get("/some-http-header-auth/")
def demo_some_http_header(
    auth_username: str = Depends(get_username_by_static_auth_token),
):

    return {
        "message": "hello",
        "username": auth_username,
    }


COOKIES: dict[str, dict[str, Any]] = {}  # Словарь с куками
COOKIES_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:  # генерим случайный id
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(
        default=None,
        alias=COOKIES_SESSION_ID_KEY,
    ),
) -> dict:
    if (session_id is None) or (session_id not in COOKIES):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not auntificated"
        )

    return COOKIES[session_id]


@router.get("/login-cookie/")
def demo_some_http_header(
    responce: Response,  # нудно для работы с куки
    auth_username: str = Depends(
        get_username_by_static_auth_token
    ),  # первоначальная проверка вообще пользователя, можно так-то и через basic_auth
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_time": int(time.time()),
    }
    responce.set_cookie(COOKIES_SESSION_ID_KEY, session_id)
    return {"Result": "OK"}


@router.get("/check_cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"hello {username}",
        **user_session_data,
    }


@router.get("/logout_cookie")
def demo_auth_logout_cookie(
    responce: Response,
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id),
    responce.delete_cookie(COOKIES_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"bye, {username}",
        **user_session_data,
    }
