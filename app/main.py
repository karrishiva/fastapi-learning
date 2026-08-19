from fastapi import FastAPI
from app.routers import todos
from app.database.connection import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    version="1.0.0"
)


app.include_router(todos.router)



