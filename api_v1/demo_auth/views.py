from typing import Annotated
from fastapi import APIRouter, Depends

from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo_auth", tags=["Demo Authh"])
security = HTTPBasic()


@router.get("/basic-auth/")
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
