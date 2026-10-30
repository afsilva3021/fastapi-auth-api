from datetime import timedelta

from api.core.security import create_access_token
from tests.conftest import SENHA_PADRAO, auth_headers, cadastrar, login


def test_login_retorna_token_bearer(client):
    cadastrar(client)

    resposta = login(client)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["token_type"] == "bearer"
    assert corpo["access_token"]


def test_login_ignora_maiusculas_no_email(client):
    cadastrar(client, email="maria@example.com")

    assert login(client, email="MARIA@Example.com").status_code == 200


def test_login_com_senha_errada_retorna_401(client):
    cadastrar(client)

    resposta = login(client, senha="senha-errada-123")

    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_login_nao_revela_se_o_email_existe(client):
    cadastrar(client)

    senha_errada = login(client, senha="senha-errada-123")
    email_inexistente = login(client, email="ninguem@example.com", senha=SENHA_PADRAO)

    assert email_inexistente.status_code == 401
    assert email_inexistente.json() == senha_errada.json()


def test_rota_protegida_sem_token_retorna_401(client):
    resposta = client.get("/usuarios/me")

    assert resposta.status_code == 401


def test_token_invalido_retorna_401(client):
    resposta = client.get("/usuarios/me", headers={"Authorization": "Bearer abc.def.ghi"})

    assert resposta.status_code == 401


def test_token_expirado_retorna_401(client):
    usuario = cadastrar(client)
    token = create_access_token(str(usuario["id"]), expires_delta=timedelta(seconds=-1))

    resposta = client.get("/usuarios/me", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 401


def test_token_de_usuario_removido_retorna_401(client):
    usuario = cadastrar(client)
    headers = auth_headers(client)
    client.delete(f"/usuarios/{usuario['id']}", headers=headers)

    resposta = client.get("/usuarios/me", headers=headers)

    assert resposta.status_code == 401
