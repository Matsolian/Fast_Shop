from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel): #основа
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):  # чтобы создавать из JSON формата
    pass


class Product(ProductBase):  # выдавать данные, по умолчанию не JSON, а SQLAlchemy объект
    model_config = ConfigDict(from_attributes=True)   # позволдяет принимать не только словари, но и объекты(благодаря флагу)
    id: int
 