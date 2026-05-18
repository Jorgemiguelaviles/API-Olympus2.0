from datetime import datetime
from unittest.mock import patch, MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException

from src.routes.routes_atividades_realizadas import (
    roteador_atividades_praticadas
)
from src.config.config_banco import get_db


# ==========================================
# Configuração da aplicação de teste
# ==========================================

app = FastAPI()

app.include_router(
    roteador_atividades_praticadas
)


# ==========================================
# Mock do banco
# ==========================================

def override_get_db():
    db_mock = MagicMock()
    yield db_mock


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ==========================================
# Teste POST - sucesso
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_cadastrar_atividade_sucesso(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.cadastrar_atividade.return_value = {
        "funcional": 1001,
        "codigo_atividade": "RUN",
        "descricao": "Corrida de 5km",
        "data_hora": datetime.now()
    }

    payload = {
        "funcional": 1001,
        "codigo_atividade": "RUN",
        "descricao": "Corrida de 5km"
    }

    response = client.post(
        "/atividades/praticadas/",
        json=payload
    )

    assert response.status_code == 201

    body = response.json()

    assert body["funcional"] == 1001
    assert body["codigo_atividade"] == "RUN"
    assert body["descricao"] == "Corrida de 5km"

    mock_instance.cadastrar_atividade.assert_called_once()


# ==========================================
# Teste POST - erro interno
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_cadastrar_atividade_erro(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.cadastrar_atividade.side_effect = HTTPException(
        status_code=500,
        detail="Erro interno"
    )

    payload = {
        "funcional": 1001,
        "codigo_atividade": "RUN",
        "descricao": "Corrida de 5km"
    }

    response = client.post(
        "/atividades/praticadas/",
        json=payload
    )

    assert response.status_code == 500

    body = response.json()

    assert body["detail"] == "Erro interno"


# ==========================================
# Teste GET por funcional - sucesso
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_por_funcional_sucesso(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_por_funcional.return_value = {
        "atividades": [
            {
                "funcional": 1001,
                "codigo_atividade": "RUN",
                "descricao": "Corrida de 5km",
                "data_hora": datetime.now()
            }
        ],
        "analise_ia": "Usuário apresenta boa evolução."
    }

    response = client.get(
        "/atividades/praticadas/1001"
    )

    assert response.status_code == 200

    body = response.json()

    assert "atividades" in body
    assert "analise_ia" in body

    assert len(body["atividades"]) == 1

    assert body["atividades"][0]["funcional"] == 1001

    mock_instance.buscar_por_funcional.assert_called_once_with(
        1001
    )


# ==========================================
# Teste GET por funcional - 404
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_por_funcional_nao_encontrado(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_por_funcional.side_effect = HTTPException(
        status_code=404,
        detail="Nenhuma atividade encontrada."
    )

    response = client.get(
        "/atividades/praticadas/1001"
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Nenhuma atividade encontrada."


# ==========================================
# Teste GET todas atividades - sucesso
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_todas_atividades_sucesso(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_todas_atividades.return_value = [
        {
            "funcional": 1001,
            "codigo_atividade": "RUN",
            "descricao": "Corrida de 5km",
            "data_hora": datetime.now()
        },
        {
            "funcional": 1002,
            "codigo_atividade": "SWIM",
            "descricao": "Natação",
            "data_hora": datetime.now()
        }
    ]

    response = client.get(
        "/atividades/praticadas/"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    assert body[0]["funcional"] == 1001
    assert body[1]["funcional"] == 1002

    mock_instance.buscar_todas_atividades.assert_called_once()


# ==========================================
# Teste GET todas atividades - vazio
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_todas_atividades_vazio(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_todas_atividades.side_effect = HTTPException(
        status_code=404,
        detail="Nenhuma atividade encontrada."
    )

    response = client.get(
        "/atividades/praticadas/"
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Nenhuma atividade encontrada."


# ==========================================
# Teste GET todas atividades - erro interno
# ==========================================

@patch(
    "src.routes.routes_atividades_realizadas.controller_atividades_realizadas"
)
def test_buscar_todas_atividades_erro(
    mock_controller
):

    mock_instance = mock_controller.return_value

    mock_instance.buscar_todas_atividades.side_effect = HTTPException(
        status_code=500,
        detail="Erro interno"
    )

    response = client.get(
        "/atividades/praticadas/"
    )

    assert response.status_code == 500

    body = response.json()

    assert body["detail"] == "Erro interno"