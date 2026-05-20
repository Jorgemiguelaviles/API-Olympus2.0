# tests/routes/test_routes_atividades_praticadas.py

from unittest.mock import MagicMock

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.routes.routes_atividades_realizadas import (
    roteador_atividades_praticadas,
    get_controller
)


# ==========================================
# APP
# ==========================================
app = FastAPI()


# ==========================================
# MIDDLEWARE MOCK USER
# ==========================================
@app.middleware("http")
async def fake_auth(
    request: Request,
    call_next
):

    request.state.user = {
        "funcional": 999
    }

    return await call_next(request)


app.include_router(
    roteador_atividades_praticadas
)


# ==========================================
# MOCK CONTROLLER
# ==========================================
mock_controller = MagicMock()

app.dependency_overrides[get_controller] = (
    lambda: mock_controller
)

client = TestClient(app)


# ==========================================
# CADASTRAR ATIVIDADE
# ==========================================
def test_cadastrar_atividade():

    mock_controller.cadastrar_atividade.return_value = {
        "status": "ok",
        "atividade": {
            "funcional": 999,
            "codigo_atividade": "SUPINO-001",
            "nome_atividade": "SUPINO",
            "data_hora": "2026-01-01T10:00:00"
        }
    }

    response = client.post(
        "/atividadespraticadas/",
        json={
            "codigo_atividade": "SUPINO-001",
            "descricao": "Treino peito"
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["status"] == "ok"

    assert (
        body["atividade"]["codigo_atividade"]
        == "SUPINO-001"
    )

    mock_controller.cadastrar_atividade.assert_called_once()


# ==========================================
# BUSCAR MINHAS ATIVIDADES
# ==========================================
def test_buscar_minhas_atividades():

    mock_controller.buscar_por_funcional.return_value = {
        "atividades": [],
        "analise_ia": {
            "status": "ok"
        }
    }

    response = client.get(
        "/atividadespraticadas/minhas"
    )

    assert response.status_code == 200

    body = response.json()

    assert "atividades" in body

    assert "analise_ia" in body

    mock_controller.buscar_por_funcional.assert_called_once_with(
        999
    )


# ==========================================
# BUSCAR TODAS
# ==========================================
def test_buscar_todas_atividades():

    mock_controller.buscar_todas_atividades.return_value = [
        {
            "funcional": 999,
            "codigo_atividade": "SUPINO-001",
            "nome_atividade": "SUPINO",
            "data_hora": "2026-01-01T10:00:00"
        }
    ]

    response = client.get(
        "/atividadespraticadas/"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1

    assert (
        body[0]["codigo_atividade"]
        == "SUPINO-001"
    )

    mock_controller.buscar_todas_atividades.assert_called_once()


# ==========================================
# VALIDAÇÃO PAYLOAD
# ==========================================
def test_cadastrar_atividade_payload_invalido():

    response = client.post(
        "/atividadespraticadas/",
        json={
            "codigo_atividade": ""
        }
    )

    assert response.status_code == 422


# ==========================================
# VALIDAÇÃO CAMPO OBRIGATÓRIO
# ==========================================
def test_cadastrar_atividade_sem_codigo():

    response = client.post(
        "/atividadespraticadas/",
        json={
            "descricao": "Treino peito"
        }
    )

    assert response.status_code == 422