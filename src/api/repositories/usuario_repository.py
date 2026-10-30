from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.db.scalar(select(Usuario).where(Usuario.email == email))

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return self.db.get(Usuario, usuario_id)

    def listar(self, skip: int = 0, limit: int = 50) -> Sequence[Usuario]:
        consulta = select(Usuario).order_by(Usuario.id).offset(skip).limit(limit)
        return self.db.scalars(consulta).all()

    def criar(self, nome: str, email: str, senha: str) -> Usuario:
        usuario = Usuario(nome=nome, email=email, senha=senha)
        self.db.add(usuario)
        self._commit()
        self.db.refresh(usuario)
        return usuario

    def atualizar(self, usuario: Usuario, campos: dict[str, str]) -> Usuario:
        for campo, valor in campos.items():
            setattr(usuario, campo, valor)
        self._commit()
        self.db.refresh(usuario)
        return usuario

    def deletar(self, usuario: Usuario) -> None:
        self.db.delete(usuario)
        self._commit()

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
