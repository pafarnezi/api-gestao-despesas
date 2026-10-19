from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
import pytest


@pytest.fixture(scope="function")
def client():
    """Cria as tabelas, disponibiliza o TestClient e limpa o banco após cada teste."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Limpa todas as tabelas para garantir isolamento entre testes
    db = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


def test_criar_despesa(client):
    response = client.post(
        "/despesas/",
        json={"descricao": "Almoço", "valor": 35.50, "categoria": "Alimentação"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["descricao"] == "Almoço"
    assert data["valor"] == 35.5
    assert data["categoria"] == "Alimentação"
    assert "id" in data
    assert "data" in data


def test_listar_despesas(client):
    client.post(
        "/despesas/",
        json={"descricao": "Transporte", "valor": 10.0, "categoria": "Transporte"},
    )
    response = client.get("/despesas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_obter_despesa_nao_encontrada(client):
    response = client.get("/despesas/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Despesa não encontrada"


def test_atualizar_despesa(client):
    criar = client.post(
        "/despesas/",
        json={"descricao": "Antiga", "valor": 1.0, "categoria": "Teste"},
    )
    despesa_id = criar.json()["id"]

    response = client.put(
        f"/despesas/{despesa_id}",
        json={"descricao": "Atualizada", "valor": 2.0, "categoria": "Teste"},
    )
    assert response.status_code == 200
    assert response.json()["descricao"] == "Atualizada"
    assert response.json()["valor"] == 2.0


def test_deletar_despesa(client):
    criar = client.post(
        "/despesas/",
        json={"descricao": "Para deletar", "valor": 5.0, "categoria": "Teste"},
    )
    despesa_id = criar.json()["id"]

    response = client.delete(f"/despesas/{despesa_id}")
    assert response.status_code == 204

    response = client.get(f"/despesas/{despesa_id}")
    assert response.status_code == 404