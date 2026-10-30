from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.core.dependencies import ServiceDep
from api.core.security import create_access_token
from api.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post("/login", response_model=Token, summary="Autentica e devolve um token JWT")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: ServiceDep,
) -> Token:
    """Use o e-mail no campo `username` (padrao OAuth2 password flow)."""
    usuario = service.autenticar(form.username, form.password)
    return Token(access_token=create_access_token(str(usuario.id)))
