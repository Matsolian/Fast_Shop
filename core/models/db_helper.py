from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(  # Движок для запуска БД
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(  # Фабрика подключений к БД
            bind=self.engine,
            autoflush=False,  # не отправлять запросы автоматически
            autocommit=False,  # не сохранять изменения автоматически
            expire_on_commit=False,  # не сбрасывать объекты после commit
        )

    def get_scoped_session(self):  # создать сессию
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:  # подключиться к сессии
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scooped_session_dependency(self) -> AsyncSession:  # подключиться к сессии
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
