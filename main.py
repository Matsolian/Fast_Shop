from fastapi import FastAPI, Path
import uvicorn
from user.view import router as user_router
from contextlib import asynccontextmanager
from core.models import Base, db_helper
from core.config import settings
from api_v1.products import router as api_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте — создаём все таблицы
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # приложение работает
    
    # При остановке — закрываем engine (освобождаем соединения)
    await db_helper.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(router=api_v1, prefix=settings.api_v1_prefix)


@app.get("/items/")
def list_items():
    return [
        "Item1",
        "Item2",
        "Item3",
    ]


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int = Path()):
    return {
        "message": "successful",
        "id": item_id,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
