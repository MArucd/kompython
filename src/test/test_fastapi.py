import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", summary="Glavniy ping", tags=["notDEFUALT"])
def read_root():
    return {"message": "WWW"}


@app.get("/test")
def test_endpoint():
    return {"status": "Работает!", "number": "MY SECOND NAME 'STILE'"}


@app.get("/my-name", tags=["раздача стиля, STILE"])
def my_name():
    return {"name": "Даниил", "project": "Парсер товаров"}


if __name__ == "__main__":
    uvicorn.run("test_fastapi:app", reload=True)
