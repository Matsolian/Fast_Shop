
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import UserRalationMixin



class Post(UserRalationMixin, Base):
    # _user_nullable = False
    # _user_id_uniq: bool = False
    _user_back_populates = "post"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
