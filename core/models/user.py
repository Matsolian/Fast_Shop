from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(length=32), unique=True)
    # Утвержадаем макисмальную длинну и  уникальность
    description: Mapped[str]
    phone: Mapped[int]

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profiles: Mapped["Profile"] = relationship(back_populates="user")
