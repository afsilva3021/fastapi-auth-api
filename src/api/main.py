from fastapi import FastAPI

from api.database.base import Base
from api.database.connection import engine

from api.models.usuario import Usuario
from api.routers import usuarios


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API FastAPI",
    version="1.0.0"
)

app.include_router(
    usuarios.router
)