# tests/routes/test_routes_atividades.py

from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.routes_atividades import (
    roteador_atividades
)


# ==========================================
# APP
# ==========================================
app = FastAPI()

app.include_router(
    roteador_atividades
)

client = TestClient(app)


# ==========================================
# BUSCAR OPÇÕES
# ==========================================
@patch(
    "src.routes.routes_atividades.controller_atividade_existente"
)
def test_buscar_opcoes_atividades(
    mock_controller_class
):

    mock_controller = MagicMock()

    mock_controller.busca_atividades.return_value = [
        {
            "codigo_atividade": "MUSC-001",
            "nome_atividade": "Musculação"
        }
    ]

    mock_controller_class.return_value = (
        mock_controller
    )

    response = client.get(
        "/atividades/opcoes"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1

    assert (
        body[0]["codigo_atividade"]
        == "MUSC-001"
    )

    mock_controller.busca_atividades.assert_called_once()


# ==========================================
# CADASTRAR OPÇÃO
# ==========================================
@patch(
    "src.routes.routes_atividades.controller_atividade_existente"
)
def test_cadastrar_opcao_atividade(
    mock_controller_class
):

    mock_controller = MagicMock()

    mock_controller.cadastrar_atividade.return_value = {
        "codigo_atividade": "NAT-001",
        "nome_atividade": "Natação"
    }

    mock_controller_class.return_value = (
        mock_controller
    )

    response = client.post(
        "/atividades/opcoes",
        json={
            "descricao": "Natação"
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert (
        body["codigo_atividade"]
        == "NAT-001"
    )

    assert (
        body["nome_atividade"]
        == "Natação"
    )

    mock_controller.cadastrar_atividade.assert_called_once_with(
        {
            "descricao": "Natação"
        }
    )


# ==========================================
# PAYLOAD INVÁLIDO
# ==========================================
def test_cadastrar_opcao_payload_invalido():

    response = client.post(
        "/atividades/opcoes",
        json={
            "descricao": "A"
        }
    )

    assert response.status_code == 422


# ==========================================
# CAMPO OBRIGATÓRIO
# ==========================================
def test_cadastrar_opcao_sem_descricao():

    response = client.post(
        "/atividades/opcoes",
        json={}
    )

    assert response.status_code == 422