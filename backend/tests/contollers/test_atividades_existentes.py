# tests/controllers/test_controller_atividades.py

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.contollers.controller_atividades import (
    controller_atividade_existente
)


# ==========================================
# FIXTURE
# ==========================================
@pytest.fixture
def db_mock():
    return MagicMock()


# ==========================================
# INIT
# ==========================================
def test_init_controller(db_mock):

    controller = controller_atividade_existente(db_mock)

    assert controller.db == db_mock
    assert controller.service_banco is not None
    assert controller.service_validacao is not None


# ==========================================
# BUSCAR ATIVIDADES - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_atividades.service_atividades"
)
@patch(
    "src.contollers.controller_atividades.service_validacao_atividade"
)
def test_busca_atividades_sucesso(
    mock_validacao,
    mock_service,
    db_mock
):

    atividades_mock = [
        {
            "codigo_atividade": "abc123",
            "nome_atividade": "NATAÇÃO"
        }
    ]

    service_instance = MagicMock()

    service_instance.buscar_todas_atividades.return_value = (
        atividades_mock
    )

    mock_service.return_value = service_instance

    controller = controller_atividade_existente(db_mock)

    resultado = controller.busca_atividades()

    assert resultado == atividades_mock

    service_instance.buscar_todas_atividades.assert_called_once()


# ==========================================
# BUSCAR ATIVIDADES - 404
# ==========================================
@patch(
    "src.contollers.controller_atividades.service_atividades"
)
def test_busca_atividades_not_found(
    mock_service,
    db_mock
):

    service_instance = MagicMock()

    service_instance.buscar_todas_atividades.return_value = []

    mock_service.return_value = service_instance

    controller = controller_atividade_existente(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.busca_atividades()

    assert erro.value.status_code == 404

    assert (
        erro.value.detail
        == "Nenhuma atividade encontrada."
    )


# ==========================================
# BUSCAR ATIVIDADES - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_atividades.service_atividades"
)
def test_busca_atividades_erro_interno(
    mock_service,
    db_mock
):

    service_instance = MagicMock()

    service_instance.buscar_todas_atividades.side_effect = (
        Exception("Falha banco")
    )

    mock_service.return_value = service_instance

    controller = controller_atividade_existente(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.busca_atividades()

    assert erro.value.status_code == 500

    assert (
        "Erro interno ao consultar atividades"
        in erro.value.detail
    )


# ==========================================
# CADASTRAR ATIVIDADE - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_atividades.service_atividades"
)
@patch(
    "src.contollers.controller_atividades.service_validacao_atividade"
)
def test_cadastrar_atividade_sucesso(
    mock_validacao,
    mock_service,
    db_mock
):

    atividade_mock = {
        "codigo_atividade": "abc123",
        "nome_atividade": "NATAÇÃO"
    }

    service_instance = MagicMock()

    service_instance.cadastrar_atividade.return_value = (
        atividade_mock
    )

    mock_service.return_value = service_instance

    validacao_instance = MagicMock()

    mock_validacao.return_value = validacao_instance

    controller = controller_atividade_existente(db_mock)

    payload = {
        "descricao": " natação "
    }

    resultado = controller.cadastrar_atividade(
        payload
    )

    assert resultado == atividade_mock

    validacao_instance.validar_cadastro.assert_called_once_with(
        payload,
        db_mock
    )

    service_instance.cadastrar_atividade.assert_called_once()

    payload_enviado = (
        service_instance.cadastrar_atividade.call_args[0][0]
    )

    assert payload_enviado["descricao"] == "NATAÇÃO"


# ==========================================
# CADASTRAR ATIVIDADE - HTTPException
# ==========================================
@patch(
    "src.contollers.controller_atividades.service_atividades"
)
@patch(
    "src.contollers.controller_atividades.service_validacao_atividade"
)
def test_cadastrar_atividade_http_exception(
    mock_validacao,
    mock_service,
    db_mock
):

    validacao_instance = MagicMock()

    validacao_instance.validar_cadastro.side_effect = (
        HTTPException(
            status_code=400,
            detail="Atividade já existe"
        )
    )

    mock_validacao.return_value = validacao_instance

    mock_service.return_value = MagicMock()

    controller = controller_atividade_existente(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.cadastrar_atividade({
            "descricao": "corrida"
        })

    assert erro.value.status_code == 400

    assert erro.value.detail == "Atividade já existe"


# ==========================================
# CADASTRAR ATIVIDADE - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_atividades.service_atividades"
)
@patch(
    "src.contollers.controller_atividades.service_validacao_atividade"
)
def test_cadastrar_atividade_erro_interno(
    mock_validacao,
    mock_service,
    db_mock
):

    validacao_instance = MagicMock()

    mock_validacao.return_value = validacao_instance

    service_instance = MagicMock()

    service_instance.cadastrar_atividade.side_effect = (
        Exception("Falha ao salvar")
    )

    mock_service.return_value = service_instance

    controller = controller_atividade_existente(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.cadastrar_atividade({
            "descricao": "corrida"
        })

    assert erro.value.status_code == 500

    assert (
        "Erro ao cadastrar atividade"
        in erro.value.detail
    )