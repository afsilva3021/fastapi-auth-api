import os

# As variaveis precisam existir antes de importar a aplicacao (Settings le o ambiente).
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "chave-apenas-para-testes-com-mais-de-32-caracteres"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["BCRYPT_ROUNDS"] = "4"  # minimo do bcrypt: deixa os testes rapidos

from collections.abc import Iterator  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import api.models  # noqa: E402, F401  (registra as tabelas no metadata)
from api.database.base import Base  # noqa: E402
from api.database.connection import get_db  # noqa: E402
from api.main import app  # noqa: E402

SENHA_PADRAO = "senha-segura-123"


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Cliente HTTP com um banco SQLite em memoria novo para cada teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    engine.dispose()


def cadastrar(client: TestClient, email: str = "maria@example.com", nome: str = "Maria Silva"):
    resposta = client.post(
        "/usuarios/",
        json={"nome": nome, "email": email, "senha": SENHA_PADRAO},
    )
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def login(client: TestClient, email: str = "maria@example.com", senha: str = SENHA_PADRAO):
    return client.post("/auth/login", data={"username": email, "password": senha})


def auth_headers(client: TestClient, email: str = "maria@example.com") -> dict[str, str]:
    resposta = login(client, email)
    assert resposta.status_code == 200, resposta.text
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}
