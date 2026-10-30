from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.core.exceptions import (
    AcessoNegado,
    CredenciaisInvalidas,
    DomainError,
    EmailJaCadastrado,
    TokenInvalido,
    UsuarioNaoEncontrado,
)

STATUS_POR_ERRO: dict[type[DomainError], int] = {
    UsuarioNaoEncontrado: status.HTTP_404_NOT_FOUND,
    EmailJaCadastrado: status.HTTP_409_CONFLICT,
    CredenciaisInvalidas: status.HTTP_401_UNAUTHORIZED,
    TokenInvalido: status.HTTP_401_UNAUTHORIZED,
    AcessoNegado: status.HTTP_403_FORBIDDEN,
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        status_code = STATUS_POR_ERRO.get(type(exc), status.HTTP_400_BAD_REQUEST)
        headers = (
            {"WWW-Authenticate": "Bearer"} if status_code == status.HTTP_401_UNAUTHORIZED else None
        )
        return JSONResponse(
            status_code=status_code,
            content={"detail": exc.detail},
            headers=headers,
        )
