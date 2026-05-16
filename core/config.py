from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    # db_echo: bool = False
    db_echo: bool = (
        True  # когда мы работаем с отладкой, мы замедляем программу и небезопасно
    )


settings = Setting()
