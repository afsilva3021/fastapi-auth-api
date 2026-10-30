from fastapi import FastAPI

from api.core.errors import register_exception_handlers
from api.routers import auth, usuarios

app = FastAPI(
    title="FastAPI Auth API",
    description="API REST de usuarios com autenticacao JWT (OAuth2 password flow).",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(usuarios.router)


@app.get("/health", tags=["Infra"], summary="Verifica se a API esta no ar")
def health() -> dict[str, str]:
    return {"status": "ok"}
