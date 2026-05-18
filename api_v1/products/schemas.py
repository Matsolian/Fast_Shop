from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel): #основа
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):  # чтобы создавать
    pass


class Product(ProductBase):  # выдавать данные
    model_config = ConfigDict(from_attributes=True)
    id: int
