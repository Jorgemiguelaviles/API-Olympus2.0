from unittest.mock import (
    Mock,
    patch
)

from fastapi import FastAPI
from fastapi.testclient import (
    TestClient
)

from src.routes.routes_analise_IA import (
    roteador_analise_ia
)

from src.contollers.controller_analise_ia import (
    controller_analise_ia
)


# ==========================================
# APP TESTE
# ==========================================
app = FastAPI()

app.include_router(
    roteador_analise_ia
)

client = TestClient(app)


# ==========================================
# TESTE ROTA
# ==========================================
def test_buscar_status_analise(
    monkeypatch
):

    retorno_mock = {

        "status": "concluido",

        "resultado": {
            "resumo": "ok"
        },

        "erro": None
    }

    def mock_buscar(
        self,
        task_id
    ):
        return retorno_mock

    monkeypatch.setattr(
        controller_analise_ia,
        "buscar_status_analise",
        mock_buscar
    )

    response = client.get(
        "/analise-ia/analise/123"
    )

    assert response.status_code == 200

    assert response.json() == retorno_mock


# ==========================================
# TESTE SUCCESS
# ==========================================
@patch(
    "src.contollers.controller_analise_ia.AsyncResult"
)
def test_buscar_status_success(
    mock_async
):

    mock_task = Mock()

    mock_task.state = "SUCCESS"

    mock_task.result = {
        "resumo": "Tudo certo"
    }

    mock_task.info = None

    mock_async.return_value = mock_task

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise("abc")
    )

    assert response["status"] == "concluido"

    assert response["resultado"] == {
        "resumo": "Tudo certo"
    }

    assert response["erro"] is None


# ==========================================
# TESTE PENDING
# ==========================================
@patch(
    "src.contollers.controller_analise_ia.AsyncResult"
)
def test_buscar_status_pending(
    mock_async
):

    mock_task = Mock()

    mock_task.state = "PENDING"

    mock_task.result = None

    mock_task.info = None

    mock_async.return_value = mock_task

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise("abc")
    )

    assert response["status"] == "processando"

    assert response["resultado"] is None

    assert response["erro"] is None
# ==========================================
# TESTE FAILURE
# ==========================================
@patch(
    "src.contollers.controller_analise_ia.AsyncResult"
)
def test_buscar_status_failure(
    mock_async
):

    mock_task = Mock()

    mock_task.state = "FAILURE"

    mock_task.result = "Erro interno"

    mock_task.info = "Erro interno"

    mock_async.return_value = mock_task

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise("abc")
    )

    assert response["status"] == "erro"

    assert response["erro"] == "Erro interno"