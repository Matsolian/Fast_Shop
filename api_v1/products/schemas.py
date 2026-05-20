from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):  # основа
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):  # чтобы создавать из JSON формата
    pass


class ProductUpdate(ProductCreate):  
    pass

class ProductUpdatePartial(ProductCreate):  
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Product(
    ProductBase
):  # выдавать данные, по умолчанию не JSON, а SQLAlchemy объект
    model_config = ConfigDict(
        from_attributes=True
    )  # позволяет принимать не только словари, но и объекты(благодаря флагу)
    id: int
