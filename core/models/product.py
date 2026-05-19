from sqlalchemy.orm import Mapped
from .base import Base

class Product(Base):
    __tablename__ = "products"  # не обязательно теперь, мы в главном Base создали проперти

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]


