from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from .base import Base
from .order_product_association import order_product_association_table

if TYPE_CHECKING:
    from .order import Order


class Product(Base):
    __tablename__ = (
        "products"  # не обязательно теперь, мы в главном Base создали проперти
    )

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(
        secondary=order_product_association_table,
        back_populates="products",
    )
