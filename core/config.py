from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_URL = BASE_DIR / "db.sqlite3"


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_URL}"
    # db_echo: bool = False
    echo: bool = (
        True
        # когда мы работаем с отладкой, мы замедляем программу и небезопасно
    )


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DBSettings = DBSettings()


settings = Settings()
