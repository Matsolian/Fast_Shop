import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

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


def get_auth_user_username(    # Проверка с админами
    credantials: Annotated[
        HTTPBasicCredentials,
        Depends(security),
    ],
):
    unauted_exc = HTTPException(  #Наша кастомная ошибка 
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


@router.get("/basic-auth_username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):

    return {
        "message": "hello",
        "username": auth_username,
    }
