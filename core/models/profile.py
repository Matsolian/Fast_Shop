from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import UserRalationMixin


class Profile(UserRalationMixin, Base):
    _user_id_uniq = True
    _user_back_populates = "profiles"

    first_name: Mapped[str | None] = mapped_column(String(length=32))
    last_name: Mapped[str | None] = mapped_column(String(length=32))
    bio: Mapped[str | None]
