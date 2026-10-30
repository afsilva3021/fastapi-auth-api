from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from api.core.dependencies import CurrentUser, ServiceDep
from api.core.exceptions import AcessoNegado
from api.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um usuario (rota publica)",
)
def criar_usuario(dados: UsuarioCreate, service: ServiceDep):
    return service.criar(dados)


@router.get("/me", response_model=UsuarioResponse, summary="Dados do usuario autenticado")
def meu_perfil(usuario_atual: CurrentUser):
    return usuario_atual


@router.get("/", response_model=list[UsuarioResponse], summary="Lista usuarios (paginado)")
def listar_usuarios(
    _: CurrentUser,
    service: ServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    return service.listar(skip=skip, limit=limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Busca um usuario por ID")
def buscar_usuario(usuario_id: int, _: CurrentUser, service: ServiceDep):
    return service.buscar_por_id(usuario_id)


@router.patch(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Atualiza parcialmente o proprio usuario",
)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    usuario_atual: CurrentUser,
    service: ServiceDep,
):
    _exigir_mesmo_usuario(usuario_id, usuario_atual.id)
    return service.atualizar(usuario_id, dados)


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove o proprio usuario",
)
def deletar_usuario(usuario_id: int, usuario_atual: CurrentUser, service: ServiceDep):
    _exigir_mesmo_usuario(usuario_id, usuario_atual.id)
    service.deletar(usuario_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _exigir_mesmo_usuario(usuario_id: int, usuario_atual_id: int) -> None:
    if usuario_id != usuario_atual_id:
        raise AcessoNegado()
