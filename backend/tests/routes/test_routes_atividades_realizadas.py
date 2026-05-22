# tests/routes/test_rotas_atividades_praticadas.py

from datetime import datetime
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.routes_atividades_realizadas import (
    roteador_atividades_praticadas,
    get_controller
)


# ==========================================
# APP MOCK
# ==========================================
app = FastAPI()

app.include_router(
    roteador_atividades_praticadas
)


# ==========================================
# MIDDLEWARE MOCK USER
# ==========================================
@app.middleware("http")
async def mock_user(
    request,
    call_next
):

    request.state.user = {
        "funcional": 999
    }

    response = await call_next(request)

    return response


# ==========================================
# FIXTURE CLIENT
# ==========================================
client = TestClient(app)


# ==========================================
# FIXTURE CONTROLLER
# ==========================================
def override_controller():

    controller = MagicMock()

    app.dependency_overrides[
        get_controller
    ] = lambda: controller

    return controller


# ==========================================
# POST /atividadespraticadas
# ==========================================
def test_cadastrar_atividade_sucesso():

    controller = override_controller()

    controller.cadastrar_atividade.return_value = {
        "status": "ok",
        "atividade": {
            "funcional": 999,
            "codigo_atividade": "SUPINO-001",
            "nome_atividade": "Supino",
            "data_hora": str(datetime.now())
        }
    }

    response = client.post(
        "/atividadespraticadas/",
        json={
            "codigo_atividade": "SUPINO-001",
            "descricao": "Supino"
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["status"] == "ok"

    controller.cadastrar_atividade.assert_called_once()

    payload = (
        controller
        .cadastrar_atividade
        .call_args[0][0]
    )

    assert payload["funcional"] == 999
    assert payload["codigo_atividade"] == "SUPINO-001"
    assert payload["descricao"] == "Supino"

    assert isinstance(
        payload["data_hora"],
        datetime
    )


# ==========================================
# POST INVALIDO
# ==========================================
def test_cadastrar_atividade_payload_invalido():

    override_controller()

    response = client.post(
        "/atividadespraticadas/",
        json={}
    )

    assert response.status_code == 422


# ==========================================
# GET /minhas
# ==========================================
def test_buscar_minhas_atividades():

    controller = override_controller()

    controller.buscar_por_funcional.return_value = {
        "atividades": [],
        "analise_ia": {
            "task_id": "123",
            "status": "processando",
            "endpoint_consulta":
            "/analise-ia/analise/123"
        }
    }

    response = client.get(
        "/atividadespraticadas/minhas"
    )

    assert response.status_code == 200

    body = response.json()

    assert "atividades" in body
    assert "analise_ia" in body

    controller.buscar_por_funcional.assert_called_once_with(
        999
    )


# ==========================================
# GET /
# ==========================================
def test_buscar_todas_atividades():

    controller = override_controller()

    controller.buscar_todas_atividades.return_value = [
        {
            "funcional": 1,
            "codigo_atividade": "SUPINO-001",
            "nome_atividade": "Supino",
            "data_hora": str(datetime.now())
        }
    ]

    response = client.get(
        "/atividadespraticadas/"
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    assert body[0]["codigo_atividade"] == (
        "SUPINO-001"
    )

    controller.buscar_todas_atividades.assert_called_once()


# ==========================================
# GET TODAS VAZIO
# ==========================================
def test_buscar_todas_atividades_vazio():

    controller = override_controller()

    controller.buscar_todas_atividades.return_value = []

    response = client.get(
        "/atividadespraticadas/"
    )

    assert response.status_code == 200

    assert response.json() == []


# ==========================================
# REMOVE OVERRIDE
# ==========================================
def teardown_module():

    app.dependency_overrides = {}