# FastAPI Auth API

[![CI](https://github.com/afsilva3021/fastapi-auth-api/actions/workflows/ci.yml/badge.svg)](https://github.com/afsilva3021/fastapi-auth-api/actions/workflows/ci.yml)

API REST de usuários com autenticação JWT, feita com **FastAPI**, **SQLAlchemy 2.0** e **Alembic**.
O projeto segue uma arquitetura em camadas (router → service → repository) e tem testes de
integração isolados, que não tocam em nenhum banco real.

## Funcionalidades

- Cadastro público de usuários e login com **OAuth2 password flow** (token JWT Bearer).
- Rotas protegidas por token; cada usuário só altera ou remove a **própria** conta (403 caso contrário).
- Senhas com hash **bcrypt**; a senha nunca aparece nas respostas.
- Validação de entrada com Pydantic (e-mail normalizado, senha de 8 a 72 bytes, nome de 2 a 100 caracteres).
- Erros de negócio tratados como exceções de domínio, convertidas para HTTP em um único lugar.
- Login que não revela se um e-mail existe (mesma resposta e tempo parecido para os dois casos).
- Paginação em `GET /usuarios/`, migrations com Alembic e suporte a SQLite e PostgreSQL.

## Tecnologias

Python 3.12+ · FastAPI · SQLAlchemy 2.0 · Alembic · Pydantic Settings · PyJWT · bcrypt ·
PostgreSQL / SQLite · pytest + HTTPX · Ruff · uv · Docker · GitHub Actions

## Estrutura

```
src/api/
├── main.py            # app FastAPI, routers e handlers de erro
├── core/              # config, segurança (bcrypt/JWT), dependências e exceções
├── database/          # engine, sessão e Base do SQLAlchemy
├── models/            # modelos ORM
├── schemas/           # contratos de entrada e saída (Pydantic)
├── repositories/      # acesso a dados
├── services/          # regras de negócio
└── routers/           # endpoints HTTP
alembic/               # migrations
tests/                 # testes de integração e unitários
```

## Endpoints

| Método | Rota                | Auth | Descrição                                   |
|--------|---------------------|------|---------------------------------------------|
| POST   | `/usuarios/`        | não  | Cadastra um usuário                         |
| POST   | `/auth/login`       | não  | Devolve o token (`username` = e-mail)       |
| GET    | `/usuarios/me`      | sim  | Dados do usuário autenticado                |
| GET    | `/usuarios/`        | sim  | Lista usuários (`skip`, `limit` até 100)    |
| GET    | `/usuarios/{id}`    | sim  | Busca um usuário por ID                     |
| PATCH  | `/usuarios/{id}`    | sim  | Atualiza parcialmente a própria conta       |
| DELETE | `/usuarios/{id}`    | sim  | Remove a própria conta (204)                |
| GET    | `/health`           | não  | Verificação de saúde                        |

Documentação interativa em `/docs` (use o botão **Authorize** com e-mail e senha).

## Como rodar localmente

Requisitos: Python 3.12+ e [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
cp .env.example .env          # depois troque o SECRET_KEY
uv run alembic upgrade head   # cria as tabelas
uv run fastapi dev src/api/main.py
```

Gere um `SECRET_KEY` seguro com:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### Exemplo de uso

```bash
# cadastro
curl -X POST localhost:8000/usuarios/ -H 'Content-Type: application/json' \
  -d '{"nome": "Maria Silva", "email": "maria@example.com", "senha": "senha-segura-123"}'

# login (o campo username recebe o e-mail)
curl -X POST localhost:8000/auth/login \
  -d 'username=maria@example.com&password=senha-segura-123'

# rota protegida
curl localhost:8000/usuarios/me -H "Authorization: Bearer <access_token>"
```

## Docker

```bash
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(48))")
docker compose up --build
```

Sobe a API em `http://localhost:8000` com PostgreSQL; as migrations rodam na inicialização.

## Testes e qualidade

```bash
uv run pytest             # usa SQLite em memória, não precisa de .env
uv run ruff check .
uv run ruff format --check .
```

A pipeline do GitHub Actions roda lint, formatação e testes em Python 3.12 e 3.13.

## Variáveis de ambiente

| Variável                      | Padrão  | Descrição                                       |
|-------------------------------|---------|-------------------------------------------------|
| `DATABASE_URL`                | —       | Ex.: `sqlite:///./db.sqlite3` ou `postgresql+psycopg://...` |
| `SECRET_KEY`                  | —       | Mínimo de 32 caracteres                         |
| `ALGORITHM`                   | `HS256` | `HS256`, `HS384` ou `HS512`                     |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`    | Validade do token                               |
| `BCRYPT_ROUNDS`               | `12`    | Custo do bcrypt (4 a 16)                        |

## Próximos passos

- Refresh token e revogação de tokens.
- Perfis de acesso (admin e usuário comum).
- Limite de tentativas de login (rate limiting).
