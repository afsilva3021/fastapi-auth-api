from tests.conftest import SENHA_PADRAO, auth_headers, cadastrar, login


def test_cadastro_retorna_201_e_nao_expoe_senha(client):
    resposta = client.post(
        "/usuarios/",
        json={"nome": "Maria Silva", "email": "maria@example.com", "senha": SENHA_PADRAO},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["email"] == "maria@example.com"
    assert "senha" not in corpo
    assert "criado_em" in corpo


def test_cadastro_normaliza_email_para_minusculas(client):
    usuario = cadastrar(client, email="Maria@Example.COM")

    assert usuario["email"] == "maria@example.com"


def test_cadastro_com_email_repetido_retorna_409(client):
    cadastrar(client, email="maria@example.com")

    resposta = client.post(
        "/usuarios/",
        json={"nome": "Outra", "email": "MARIA@example.com", "senha": SENHA_PADRAO},
    )

    assert resposta.status_code == 409


def test_cadastro_rejeita_dados_invalidos(client):
    base = {"nome": "Maria", "email": "maria@example.com", "senha": SENHA_PADRAO}
    invalidos = [
        {**base, "senha": "curta"},
        {**base, "senha": "a" * 73},
        {**base, "senha": "á" * 40},  # 80 bytes em UTF-8
        {**base, "email": "nao-e-email"},
        {**base, "nome": "M"},
    ]

    for payload in invalidos:
        assert client.post("/usuarios/", json=payload).status_code == 422, payload


def test_meu_perfil(client):
    cadastrar(client)

    resposta = client.get("/usuarios/me", headers=auth_headers(client))

    assert resposta.status_code == 200
    assert resposta.json()["email"] == "maria@example.com"


def test_listar_exige_autenticacao(client):
    assert client.get("/usuarios/").status_code == 401


def test_listar_com_paginacao(client):
    for indice in range(3):
        cadastrar(client, email=f"user{indice}@example.com", nome=f"Usuario {indice}")
    headers = auth_headers(client, email="user0@example.com")

    todos = client.get("/usuarios/", headers=headers).json()
    pagina = client.get("/usuarios/?skip=1&limit=1", headers=headers).json()

    assert len(todos) == 3
    assert [u["id"] for u in pagina] == [todos[1]["id"]]


def test_listar_rejeita_limite_invalido(client):
    cadastrar(client)

    resposta = client.get("/usuarios/?limit=1000", headers=auth_headers(client))

    assert resposta.status_code == 422


def test_buscar_por_id(client):
    usuario = cadastrar(client)
    headers = auth_headers(client)

    assert client.get(f"/usuarios/{usuario['id']}", headers=headers).status_code == 200
    assert client.get("/usuarios/9999", headers=headers).status_code == 404


def test_atualizar_proprio_usuario_parcialmente(client):
    usuario = cadastrar(client)
    headers = auth_headers(client)

    resposta = client.patch(
        f"/usuarios/{usuario['id']}", json={"nome": "Maria Souza"}, headers=headers
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Maria Souza"
    assert resposta.json()["email"] == "maria@example.com"


def test_atualizar_senha_permite_login_com_a_nova(client):
    usuario = cadastrar(client)
    headers = auth_headers(client)

    client.patch(f"/usuarios/{usuario['id']}", json={"senha": "nova-senha-456"}, headers=headers)

    assert login(client, senha=SENHA_PADRAO).status_code == 401
    assert login(client, senha="nova-senha-456").status_code == 200


def test_atualizar_para_email_ja_usado_retorna_409(client):
    usuario = cadastrar(client, email="maria@example.com")
    cadastrar(client, email="joao@example.com", nome="Joao")
    headers = auth_headers(client, email="maria@example.com")

    resposta = client.patch(
        f"/usuarios/{usuario['id']}", json={"email": "joao@example.com"}, headers=headers
    )

    assert resposta.status_code == 409


def test_atualizar_sem_campos_ou_com_nulos_retorna_422(client):
    usuario = cadastrar(client)
    headers = auth_headers(client)
    url = f"/usuarios/{usuario['id']}"

    assert client.patch(url, json={}, headers=headers).status_code == 422
    assert client.patch(url, json={"nome": None}, headers=headers).status_code == 422


def test_nao_pode_alterar_outro_usuario(client):
    cadastrar(client, email="maria@example.com")
    outro = cadastrar(client, email="joao@example.com", nome="Joao")
    headers = auth_headers(client, email="maria@example.com")

    resposta = client.patch(f"/usuarios/{outro['id']}", json={"nome": "Hack"}, headers=headers)

    assert resposta.status_code == 403


def test_deletar_proprio_usuario(client):
    usuario = cadastrar(client)
    headers = auth_headers(client)

    resposta = client.delete(f"/usuarios/{usuario['id']}", headers=headers)

    assert resposta.status_code == 204
    assert login(client).status_code == 401


def test_nao_pode_deletar_outro_usuario(client):
    cadastrar(client, email="maria@example.com")
    outro = cadastrar(client, email="joao@example.com", nome="Joao")
    headers = auth_headers(client, email="maria@example.com")

    resposta = client.delete(f"/usuarios/{outro['id']}", headers=headers)

    assert resposta.status_code == 403


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
