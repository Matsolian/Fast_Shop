from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=settings.db_echo,
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine,  # какой движок использовать
            autoflush=False,  # не отправлять запросы автоматически
            autocommit=False,  # не сохранять изменения автоматически
            expire_on_commit=False,  # не сбрасывать объекты после commit
        )


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
