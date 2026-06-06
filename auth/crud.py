from fastapi.security import OAuth2PasswordBearer

from auth import utils as auth_utils
from user.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/JWT/jwt/login",  # вставляем путь для нашей  авторизации
)
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
