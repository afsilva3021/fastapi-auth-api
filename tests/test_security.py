import pytest

from api.core.exceptions import TokenInvalido
from api.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_nao_guarda_senha_em_texto_puro_e_verifica():
    hashed = hash_password("senha-segura-123")

    assert hashed != "senha-segura-123"
    assert verify_password("senha-segura-123", hashed)
    assert not verify_password("outra-senha-123", hashed)


def test_hashes_da_mesma_senha_sao_diferentes():
    assert hash_password("senha-segura-123") != hash_password("senha-segura-123")


def test_verificar_senha_acima_de_72_bytes_retorna_false_sem_erro():
    hashed = hash_password("senha-segura-123")

    assert verify_password("a" * 100, hashed) is False


def test_token_ida_e_volta():
    token = create_access_token("42")

    assert decode_access_token(token) == "42"


def test_token_adulterado_e_rejeitado():
    token = create_access_token("42")

    with pytest.raises(TokenInvalido):
        decode_access_token(token[:-2] + "xx")
