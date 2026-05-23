"""
CRUD USERS
"""

import asyncio
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from core.models import db_helper, User, Profile, Post, OrderProductAssociation
from core.models.order import Order


async def create_user(sesion: AsyncSession, username: str) -> User:
    user = User(username=username)
    sesion.add(user)
    await sesion.commit()
    print("user", user)
    return user


async def get_user_by_username(sesion: AsyncSession, username) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await sesion.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profile(
    session: AsyncSession,
) -> list[User]:
    stmt = select(User).options(joinedload(User.profiles)).order_by(User.id)
    # Из-за того, что это ассинхронный подход, то надо сразу подгрузить профили
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        if user.profiles:
            print(user.profiles.first_name)
        else:
            print("User don't have profile")


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print("Post created")
    return posts


async def get_users_with_posts(  # Один ко многим
    session: AsyncSession,
):

    stmt = (
        select(User)
        .options(
            selectinload(User.posts),  # подход 3
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)  # подход 1 and 3
    result: Result = await session.execute(stmt)

    for user in users:  # type: user
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = select(User).options(
        joinedload(User.profiles),
        selectinload(User.posts),
    )
    users = await session.scalars(stmt)

    for user in users:
        print("**" * 10)
        print(user, user.profiles and user.profiles.first_name)  # Однострочник проверка
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "Rock")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode="promo")
    order_1 = await create_product(
        session,
        name="Beard",
        description="tasty beard",
        price=89,
    )
    order_2 = await create_product(
        session,
        name="Milk",
        description="tasty milk",
        price=230,
    )
    order_3 = await create_product(
        session,
        name="Chips",
        description="tasty Chips",
        price=259,
    )
    # мы обращаемся к order, а он обращается к product. Надо подгрузить все поля
    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order_one.products.append(order_2)
    order_one.products.append(order_1)
    order_promo.products.append(order_3)
    order_promo.products.append(order_1)
    order_promo.products.append(order_2)

    await session.commit()


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    # await create_orders_and_products(session)
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_data, "products:")
        for product in order.products:  # type: ignore # type: Product
            print("-", product.id, product.name, product.price)


async def main_ralations(session: AsyncSession):
    # await create_user(sesion=session, username="Bob")
    # # await create_user(sesion=session, username="Rock")
    # user_bob = await get_user_by_username(sesion=session, username="Bob")
    # user_john = await get_user_by_username(sesion=session, username="John")
    # user_rock = await get_user_by_username(sesion=session, username="Rock")
    # await create_user_profile(
    #     session=session,
    #     user_id=user_john.id,
    #     first_name="John",
    # )
    # await create_user_profile(
    #     session=session,
    #     user_id=user_bob.id,
    #     first_name="Luci",
    # )
    # await show_users_with_profile(session=session)
    # await create_posts(session, user_bob.id, "Hello my friends")
    # await create_posts(session, user_john.id, "I learned Fast API")
    # await get_users_with_posts(session=session)
    # await get_users_with_posts_and_profiles(session=session)
    # await get_profiles_with_users_with_posts(session=session)
    pass


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)

    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
    )

    session.add(product)
    await session.commit()
    return product


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.product_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)

    for order in orders:
        print(order.id, order.promocode, order.created_data, "products:")
        for (
            order_product_details
        ) in order.product_details:  # Type: OrderProductAssociation
            print(
                "-",
                order_product_details.product.name,
                order_product_details.product.price,
                "qty",
                order_product_details.count,
            )


async def create_gift_product_for_existing_orders(session: AsyncSession):
    await demo_get_orders_with_products_with_assoc(session)
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session,
        name="Gifr",
        description="Gift 4 you",
        price=0,
    )
    for order in orders:
        order.product_details.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )  # ни у кого нет, поэтому в наглую добавляем все
    await session.commit()


async def demo_m2m(session: AsyncSession):  # many to many
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)
    # await create_gift_product_for_existing_orders(session)



async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
