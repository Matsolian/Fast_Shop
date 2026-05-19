from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from .schemas import ProductCreate


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)  # Строим SQL-запрос.
    result: Result = await session.execute(stmt)  # Вот здесь реально идём в БД.
    products = result.scalars().all()  # Достали объекты Product из ответа
    return list(products)


# result.scalars().all() — немного странное место. Объясняю:
#   - session.execute() возвращает таблицу с колонками (даже если колонка одна)
#   - .scalars() говорит: "меня интересует только первая колонка — сам объект Product"
#   - .all() — "забери все строки сразу"


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())  # Pydantic → SQLAlchemy объект
    session.add(product)  # Добавить в очередь на запись
    await session.commit()  # Реально записать в БД
    # await session.refresh(Product) если надо будет пересобрать
    return product


#  product_in.model_dump() превращает Pydantic-схему в словарь: {"name": "Apple", "price": 100}. Затем ** распаковывает его в аргументы конструктора
#   SQLAlchemy-модели.
