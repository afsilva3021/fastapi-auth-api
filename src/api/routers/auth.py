from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Usuario
from api.schemas import LoginRequest, Token
from api.core.security import (verify_password, create_access_token)

router = APIRouter (prefix = "/auth", tags = ['Autenticacão'])

@router.post(
    "/login",
    response_model=Token
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    if not verify_password(
        dados.senha,
        usuario.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    token = create_access_token({"sub": str(usuario.id), "email": usuario.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }