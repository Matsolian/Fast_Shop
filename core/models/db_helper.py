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

    # Блок работы с API
    def get_scoped_session(self):  # создать сессию. Менеджер по официантам
        # это умная фабрика сессий. Она знает: "один asyncio-task = одна сессия". Если в рамках одного запроса ты трижды попросишь
        #   сессию — она трижды вернёт одну и ту же сессию, а не создаст три.
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    # код ДО yield → выполнить, отдать значение в хэндлер → хэндлер работает → код ПОСЛЕ yield → выполнить (очистка)
    # Аналогия: Официант берёт поднос (открывает сессию), несёт блюдо клиенту (хэндлер выполняется), потом возвращается и моет поднос (закрывает сессию).
    async def session_dependency(self) -> AsyncSession:  # подключиться к сессии
        async with self.session_factory() as session:  # открыть сессию
            yield session  # отдать в хэндлер
            await session.close()  # закрыть после

    async def scooped_session_dependency(self) -> AsyncSession:  # подключиться к сессии
        # Процесс смены: менеджер выдаёт официанта → официант работает → смена закончилась, официант свободен
        session = self.get_scoped_session()  # получить умную scoped-сессию. То есть у менеджера спросить а за каким столиком?
        yield session  # отдать в хэндлер
        await session.close()  # закрыть после запроса. Официант снова свободен

    # Конец работы с API


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
