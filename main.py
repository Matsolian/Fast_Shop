from fastapi import FastAPI, Path
import uvicorn
from user.view import router as user_router

app = FastAPI()
app.include_router(user_router)


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
