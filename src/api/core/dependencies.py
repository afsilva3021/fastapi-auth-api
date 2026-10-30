from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.core.exceptions import TokenInvalido, UsuarioNaoEncontrado
from api.core.security import decode_access_token
from api.database.connection import get_db
from api.models.usuario import Usuario
from api.repositories.usuario_repository import UsuarioRepository
from api.services.usuario_service import UsuarioService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_usuario_service(db: Annotated[Session, Depends(get_db)]) -> UsuarioService:
    return UsuarioService(UsuarioRepository(db))


ServiceDep = Annotated[UsuarioService, Depends(get_usuario_service)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: ServiceDep,
) -> Usuario:
    subject = decode_access_token(token)
    try:
        return service.buscar_por_id(int(subject))
    except (ValueError, UsuarioNaoEncontrado) as exc:
        # Token valido de um usuario que nao existe mais (ou `sub` malformado).
        raise TokenInvalido() from exc


CurrentUser = Annotated[Usuario, Depends(get_current_user)]
