from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


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


async def update_product(
    session: AsyncSession, product: Product, product_update: ProductUpdate
) -> ProductUpdate:  # через put. ПОлностью заменяю все строки
    for name, value in product_update.model_dump().items():
        setattr(product, name, value)
    await session.commit()
    return product


async def update_product_partial(
    session: AsyncSession, product: Product, product_update: ProductUpdatePartial
):  # Через Patch. Заменяю. лишь нужный атрибут
    for name, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, name, value)
    await session.commit()
    return product


# Либо можещь объяединить, они ведь релаьно похожи... Но зато в partial можешь отедльно добавлять логику, если надо
# async def update_product_partial_togetsher_mega_super(
#     session: AsyncSession, product: Product, product_update: ProductUpdate | ProductUpdatePartial, partial = False
# ) -> ProductUpdate:  # через put. ПОлностью заменяю все строки
#     for name, value in product_update.model_dump(exclude_unset=partial).items():
#         setattr(product, name, value)
#     await session.commit()
#     return product


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()  #Необязательно, оно и так сохрпанится по умолчанию