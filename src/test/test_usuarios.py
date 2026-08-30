import time
import uuid

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_cadastrar_100_usuarios():

    tempos = []

    quantidade = 100

    inicio_total = time.perf_counter()

    for i in range(1, quantidade + 1):

        email = f"usuario-{uuid.uuid4()}@teste.com"

        inicio = time.perf_counter()

        response = client.post(
            "/usuarios/",
            json={
                "nome": f"Usuario {i}",
                "email": email,
                "senha": "123456"
            }
        )

        fim = time.perf_counter()

        assert response.status_code == 200

        tempos.append(fim - inicio)

    fim_total = time.perf_counter()

    tempo_total = fim_total - inicio_total
    tempo_medio = sum(tempos) / len(tempos)
    cadastros_por_segundo = quantidade / tempo_total

    print("\n===== BENCHMARK 100 USUÁRIOS =====")
    print(f"Usuários cadastrados: {quantidade}")
    print(f"Tempo total:           {tempo_total:.4f}s")
    print(f"Tempo médio:           {tempo_medio:.4f}s")
    print(f"Mais rápido:           {min(tempos):.4f}s")
    print(f"Mais lento:            {max(tempos):.4f}s")
    print(f"Cadastros por segundo: {cadastros_por_segundo:.2f}")