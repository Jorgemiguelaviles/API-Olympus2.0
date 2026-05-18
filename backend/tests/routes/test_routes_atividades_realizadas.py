from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.routes_atividades_realizadas import (
    roteador_atividades_praticadas
)


# ==========================================
# APP TESTE
# ==========================================

app = FastAPI()

app.include_router(
    roteador_atividades_praticadas
)

client = TestClient(app)


# ==========================================
# POST
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_cadastrar_atividade(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.cadastrar_atividade.return_value = None

    payload = {
        "funcional": 123456789,
        "codigo_atividade": "1",
        "descricao": "Treino de peito"
    }

    response = client.post(
        "/atividades/praticadas/",
        json=payload
    )

    assert response.status_code == 201


# ==========================================
# GET FUNCIONAL
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_por_funcional(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_por_funcional.return_value = [
        {
            "funcional": 123456789,
            "codigo_atividade": "1",
            "descricao": "Treino",
            "data_hora": "2026-05-17T14:30:00"
        }
    ]

    response = client.get(
        "/atividades/praticadas/123456789"
    )

    assert response.status_code == 200


# ==========================================
# GET TODOS
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_todas_atividades(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_todas_atividades.return_value = [
        {
            "funcional": 123456789,
            "codigo_atividade": "1",
            "descricao": "Treino A",
            "data_hora": "2026-05-17T14:30:00"
        },
        {
            "funcional": 987654321,
            "codigo_atividade": "2",
            "descricao": "Treino B",
            "data_hora": "2026-05-17T15:30:00"
        }
    ]

    response = client.get(
        "/atividades/praticadas/"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2