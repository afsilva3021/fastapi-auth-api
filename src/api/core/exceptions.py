class DomainError(Exception):
    """Erro de regra de negocio. A camada HTTP decide o status de cada um."""

    detail = "Erro na operacao"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.detail
        super().__init__(self.detail)


class UsuarioNaoEncontrado(DomainError):
    detail = "Usuario nao encontrado"


class EmailJaCadastrado(DomainError):
    detail = "E-mail ja cadastrado"


class CredenciaisInvalidas(DomainError):
    detail = "E-mail ou senha invalidos"


class TokenInvalido(DomainError):
    detail = "Token invalido ou expirado"


class AcessoNegado(DomainError):
    detail = "Voce nao tem permissao para esta operacao"
