from fastapi import FastAPI, Path
import uvicorn
from user.view import router as user_router
from contextlib import asynccontextmanager
from core.config import settings
from api_v1.products import router as api_v1
from api_v1.demo_auth import router as api_v1_auth


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(router=api_v1, prefix=settings.api_v1_prefix)
app.include_router(router=api_v1_auth, prefix=settings.api_v1_prefix)


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
