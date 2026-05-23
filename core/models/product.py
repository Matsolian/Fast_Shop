from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .order_product_association import OrderProductAssociation


class Product(Base):
    __tablename__ = (
        "products"  # не обязательно теперь, мы в главном Base создали проперти
    )

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(
        secondary="order_product_association",
        back_populates="products",
    )

    order_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
