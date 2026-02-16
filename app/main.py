from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.connection import create_db_and_tables
from app.presentation.routers import categories, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается. Создаем базу данных...")
    await create_db_and_tables()
    print("База данных инициализирована.")
    yield
    print("Приложение завершает работу.")


app = FastAPI(title="My Blog API - Onion Architecture", lifespan=lifespan)

app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Blog API with Onion Architecture"}
