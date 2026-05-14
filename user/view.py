from fastapi import APIRouter

from user import crud
from user.schemas import Create_User

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/register")
def create_user(user: Create_User):
    return crud.create_user(user_in=user)
