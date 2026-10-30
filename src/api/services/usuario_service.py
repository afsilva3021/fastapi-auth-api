from collections.abc import Sequence
from functools import lru_cache

from sqlalchemy.exc import IntegrityError

from api.core.exceptions import (
    CredenciaisInvalidas,
    EmailJaCadastrado,
    UsuarioNaoEncontrado,
)
from api.core.security import hash_password, verify_password
from api.models.usuario import Usuario
from api.repositories.usuario_repository import UsuarioRepository
from api.schemas.usuario import UsuarioCreate, UsuarioUpdate


@lru_cache
def _hash_ficticio() -> str:
    # Usado quando o e-mail nao existe, para que o login gaste o mesmo tempo
    # nos dois casos e nao revele quais e-mails estao cadastrados.
    return hash_password("senha-ficticia")


class UsuarioService:
    def __init__(self, repository: UsuarioRepository) -> None:
        self.repository = repository

    def criar(self, dados: UsuarioCreate) -> Usuario:
        if self.repository.buscar_por_email(dados.email):
            raise EmailJaCadastrado()

        try:
            return self.repository.criar(
                nome=dados.nome,
                email=dados.email,
                senha=hash_password(dados.senha),
            )
        except IntegrityError as exc:
            # Outra requisicao cadastrou o mesmo e-mail entre a checagem e o insert.
            raise EmailJaCadastrado() from exc

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        usuario = self.repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontrado()
        return usuario

    def listar(self, skip: int = 0, limit: int = 50) -> Sequence[Usuario]:
        return self.repository.listar(skip=skip, limit=limit)

    def atualizar(self, usuario_id: int, dados: UsuarioUpdate) -> Usuario:
        usuario = self.buscar_por_id(usuario_id)
        campos = dados.model_dump(exclude_unset=True)

        novo_email = campos.get("email")
        if (
            novo_email
            and novo_email != usuario.email
            and self.repository.buscar_por_email(novo_email)
        ):
            raise EmailJaCadastrado()

        if "senha" in campos:
            campos["senha"] = hash_password(campos["senha"])

        try:
            return self.repository.atualizar(usuario, campos)
        except IntegrityError as exc:
            raise EmailJaCadastrado() from exc

    def deletar(self, usuario_id: int) -> None:
        usuario = self.buscar_por_id(usuario_id)
        self.repository.deletar(usuario)

    def autenticar(self, email: str, senha: str) -> Usuario:
        usuario = self.repository.buscar_por_email(email.strip().lower())
        hash_armazenado = usuario.senha if usuario else _hash_ficticio()
        senha_correta = verify_password(senha, hash_armazenado)

        if usuario is None or not senha_correta:
            raise CredenciaisInvalidas()
        return usuario
