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
            autoflush=False,  # не отправлять запросы автоматически
            autocommit=False,  # не сохранять изменения автоматически
            expire_on_commit=False,  # не сбрасывать объекты после commit
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.get_scoped_session() as session:
            yield session
            await session.remove()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
