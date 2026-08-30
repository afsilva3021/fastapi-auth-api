from fastapi import HTTPException

from api.repositories.usuario_repository import UsuarioRepository
from api.schemas.usuario import UsuarioCreate
from api.core.security import hash_password


class UsuarioService:

    def __init__(self, repository: UsuarioRepository):

        self.repository = repository


    def criar(self, dados: UsuarioCreate):
        usuario_existente = (
            self.repository.buscar_por_email(
                dados.email
                )
            )

        if (usuario_existente):

            raise HTTPException(
                status_code=400,
                detail = "E-mail já cadastrado"
            )

        senha_hash = hash_password(
            dados.senha
        )

        return self.repository.criar(
            nome = dados.nome,
            email = dados.email,
            senha = senha_hash
        )

    def buscar_por_id(self, usuario_id: int):

        usuario = (
            self.repository.buscar_por_id(
                usuario_id
            )
        )

        if (not usuario):

            raise HTTPException(
                status_code = 404,
                detail = "Usuário não encontrado"
            )

        return usuario

    def listar(self):

        return self.repository.listar()

    def atualizar(self, usuario_id: int, dados: UsuarioCreate):

        usuario = self.buscar_por_id(
            usuario_id
        )

        senha_hash = hash_password(
            dados.senha
        )

        return self.repository.atualizar(
            usuario,
            dados.nome,
            dados.email,
            senha_hash
        )

    def deletar(self, usuario_id: int):

        usuario = self.buscar_por_id(
            usuario_id
        )

        self.repository.deletar(usuario)