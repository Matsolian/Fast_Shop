from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from .schemas import ProductCreate


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)  # Строим SQL-запрос.
    result: Result = await session.execute(stmt)  # Вот здесь реально идём в БД.
    products = (
        result.scalars().all()
    )  # scalars() говорит "достань мне первый столбец из каждой строки" (то есть объект Product). .all() — забери все сразу в список
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(Product)
    return product
