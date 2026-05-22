from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from datetime import datetime


class Order(Base):

    promocod: Mapped[str | None]
    created_data: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
