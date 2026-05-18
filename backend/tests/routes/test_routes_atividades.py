from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.routes_atividades import (
    roteador_atividades
)


# ==========================================
# APP DE TESTE
# ==========================================

app = FastAPI()

app.include_router(
    roteador_atividades
)

client = TestClient(
    app
)


# ==========================================
# GET /atividades/opcoes
# ==========================================

@patch(
    "src.routes.routes_atividades.controller_atividade_existente"
)
def test_buscar_opcoes_atividades(
    mock_controller
):

    mock_instance = (
        mock_controller.return_value
    )

    mock_instance.gerencia_atividades.return_value = [
        {
            "codigo_atividade": "1",
            "nome_atividade": "Corrida"
        },
        {
            "codigo_atividade": "2",
            "nome_atividade": "Musculação"
        }
    ]

    response = client.get(
        "/atividades/opcoes"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    assert body[0]["codigo_atividade"] == "1"
    assert body[0]["nome_atividade"] == "Corrida"

    assert body[1]["codigo_atividade"] == "2"
    assert body[1]["nome_atividade"] == "Musculação"


# ==========================================
# Controller chamado
# ==========================================

@patch(
    "src.routes.routes_atividades.controller_atividade_existente"
)
def test_controller_foi_chamado(
    mock_controller
):

    mock_instance = (
        mock_controller.return_value
    )

    mock_instance.gerencia_atividades.return_value = [
        {
            "codigo_atividade": "1",
            "nome_atividade": "Corrida"
        }
    ]

    response = client.get(
        "/atividades/opcoes"
    )

    assert response.status_code == 200

    mock_controller.assert_called_once()

    mock_instance.gerencia_atividades.assert_called_once()