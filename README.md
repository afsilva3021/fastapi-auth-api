# API FastAPI

API REST para gerenciamento de usuarios, desenvolvida com FastAPI, SQLAlchemy e SQLite.

## Tecnologias

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic Settings
- Uvicorn
- Pytest e HTTPX
- uv

## Requisitos

- Python 3.14 ou superior
- [uv](https://docs.astral.sh/uv/)

## Instalacao

Instale as dependencias, incluindo as de desenvolvimento:

```bash
uv sync --all-groups
```

## Configuracao

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///./db.sqlite3
SECRET_KEY=troque-esta-chave-por-uma-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

O arquivo `.env` contem informacoes locais e sensiveis, por isso nao deve ser versionado.

## Executar a API

Inicie o servidor de desenvolvimento:

```bash
uv run fastapi dev src/api/main.py
```

Com a API em execucao, acesse:

- Documentacao interativa: `http://127.0.0.1:8000/docs`
- Documentacao alternativa: `http://127.0.0.1:8000/redoc`

## Endpoints

| Metodo | Rota | Descricao |
| --- | --- | --- |
| POST | `/usuarios/` | Cria um usuario |
| GET | `/usuarios/` | Lista usuarios |
| GET | `/usuarios/{usuario_id}` | Busca um usuario por ID |
| PUT | `/usuarios/{usuario_id}` | Atualiza um usuario |
| DELETE | `/usuarios/{usuario_id}` | Remove um usuario |

Exemplo de corpo para criar ou atualizar um usuario:

```json
{
	"nome": "Maria Silva",
	"email": "maria@example.com",
	"senha": "senha-segura"
}
```

## Testes

Execute os testes com:

```bash
uv run pytest
```

O teste atual usa `fastapi.testclient.TestClient` para enviar requisicoes a aplicacao e validar o cadastro de 100 usuarios. Ele tambem exibe metricas de tempo, portanto funciona como teste de integracao simples com um pequeno benchmark. Como utiliza a configuracao da aplicacao, os cadastros sao persistidos no banco definido em `DATABASE_URL`.

Para visualizar as metricas impressas pelo teste:

```bash
uv run pytest -s
```
