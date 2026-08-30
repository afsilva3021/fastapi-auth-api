from fastapi import Depends
from sqlalchemy.orm import Session

from api.database.connection import get_db
from api.repositories.usuario_repository import UsuarioRepository
from api.services.usuario_service import UsuarioService



def get_usuario_service(db: Session = Depends(get_db)):

    repository = UsuarioRepository(db)

    return UsuarioService(repository)