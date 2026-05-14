from fastapi import FastAPI, Path, Body  # Импортируем Path вместо Body
from pydantic import EmailStr
import uvicorn

app = FastAPI()


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

@app.post("/users/")
def create_user(email: EmailStr = Body()):
    return {
        "message": "success",
        "email": email,

    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)