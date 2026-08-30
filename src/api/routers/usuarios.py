from fastapi import APIRouter, Depends

from api.core.dependencies import get_usuario_service
from api.schemas.usuario import (UsuarioCreate, UsuarioResponse)
from api.services.usuario_service import UsuarioService


router = APIRouter(
    prefix = "/usuarios",
    tags = ["USuarios"]
)

@router.post("/", response_model = UsuarioResponse)
def criar_usuario(dados: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):

    return service.criar(
        dados
    )


@router.get("/", response_model = list[UsuarioResponse])
def listar_usuarios(service: UsuarioService = Depends(get_usuario_service)):

    return service.listar()


@router.get("/{usuario_id}", response_model = UsuarioResponse)
def buscar_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):

    return service.buscar_por_id(
        usuario_id
    )

@router.put("/{usuario_id}", response_model = UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):

    return service.atualizar(
        usuario_id,
        dados
    )

@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):

    service.deletar(usuario_id)

    return {
        "message": "Usuario excluido com sucesso"
    }
    