from user.schemas import Create_User


def create_user(user_in: Create_User):
    user = user_in.model_dump()
    return {
        "message": "success",
        "email": user,
    }
