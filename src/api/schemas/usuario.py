from datetime import datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    model_validator,
)

BCRYPT_MAX_BYTES = 72


def _normalizar_email(valor: str) -> str:
    valor = valor.strip().lower()
    if len(valor) > 150:
        raise ValueError("O e-mail deve ter no maximo 150 caracteres")
    return valor


def _validar_senha(valor: str) -> str:
    if len(valor.encode("utf-8")) > BCRYPT_MAX_BYTES:
        raise ValueError("A senha deve ter no maximo 72 bytes")
    return valor


Nome = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=100)]
Email = Annotated[EmailStr, AfterValidator(_normalizar_email)]
Senha = Annotated[
    str,
    StringConstraints(min_length=8),
    AfterValidator(_validar_senha),
]


class UsuarioCreate(BaseModel):
    nome: Nome
    email: Email
    senha: Senha


class UsuarioUpdate(BaseModel):
    nome: Nome | None = None
    email: Email | None = None
    senha: Senha | None = None

    @model_validator(mode="after")
    def exigir_algum_campo(self) -> "UsuarioUpdate":
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar")
        if any(getattr(self, campo) is None for campo in self.model_fields_set):
            raise ValueError("Os campos informados nao podem ser nulos")
        return self


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    criado_em: datetime
