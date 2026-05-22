"""
CRUD USERS
"""

import asyncio
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post


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
    stmt = (
        select(User).options(joinedload(User.profiles)).order_by(User.id)
    )  # Из-за того, что это ассинхронный подход, то надо сразу подгрузить профили
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        if user.profiles:
            print(user.profiles.first_name)
        else:
            print("User don't have profile")

async def main():
    async with db_helper.session_factory() as session:
        # # await create_user(sesion=session, username="Bob")
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
        await show_users_with_profile(session=session)


if __name__ == "__main__":
    asyncio.run(main())
