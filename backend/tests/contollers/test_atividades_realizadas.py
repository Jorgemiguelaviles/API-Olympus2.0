# tests/controllers/test_controller_atividades_realizadas.py

import pytest

from unittest.mock import Mock, patch

from fastapi import HTTPException

from src.contollers.controller_atividades_realizadas import (
    controller_atividades_realizadas
)


# ==========================================
# buscar_todas_atividades
# ==========================================

@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_todas_atividades_sucesso(
    mock_service
):

    db_mock = Mock()

    atividades_mock = [
        {
            "funcional": 1001,
            "descricao": "Corrida"
        }
    ]

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_todas_atividades.return_value = (
        atividades_mock
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    response = controller.buscar_todas_atividades()

    assert response == atividades_mock


@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_todas_atividades_vazio(
    mock_service
):

    db_mock = Mock()

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_todas_atividades.return_value = []

    controller = controller_atividades_realizadas(
        db_mock
    )

    with pytest.raises(HTTPException) as erro:

        controller.buscar_todas_atividades()

    assert erro.value.status_code == 404

    assert (
        erro.value.detail
        == "Nenhuma atividade encontrada."
    )


@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_todas_atividades_erro_interno(
    mock_service
):

    db_mock = Mock()

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_todas_atividades.side_effect = (
        Exception("Erro banco")
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    with pytest.raises(HTTPException) as erro:

        controller.buscar_todas_atividades()

    assert erro.value.status_code == 500

    assert (
        "Erro interno ao consultar atividades"
        in erro.value.detail
    )


# ==========================================
# buscar_por_funcional
# ==========================================

@patch(
    "src.contollers.atividades_realizadas.os.getenv"
)
@patch(
    "src.contollers.atividades_realizadas.service_gemini"
)
@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_sucesso(
    mock_service,
    mock_gemini,
    mock_getenv
):

    db_mock = Mock()

    mock_getenv.return_value = "fake_key"

    atividades_mock = [
        {
            "funcional": 1001,
            "descricao": "Corrida 5km"
        }
    ]

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_atividades_por_funcional.return_value = (
        atividades_mock
    )

    instancia_gemini = mock_gemini.return_value

    instancia_gemini.analisa_dados.return_value = (
        "Usuário evoluindo."
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    response = controller.buscar_por_funcional(
        1001
    )

    assert (
        response["atividades"]
        == atividades_mock
    )

    assert (
        response["analise_ia"]
        == "Usuário evoluindo."
    )


@patch(
    "src.contollers.atividades_realizadas.os.getenv"
)
@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_sem_api_key(
    mock_service,
    mock_getenv
):

    db_mock = Mock()

    mock_getenv.return_value = None

    atividades_mock = [
        {
            "funcional": 1001,
            "descricao": "Corrida 5km"
        }
    ]

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_atividades_por_funcional.return_value = (
        atividades_mock
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    response = controller.buscar_por_funcional(
        1001
    )

    assert (
        response["analise_ia"]
        == "API_KEY_GEMINI não configurada. Análise de IA não realizada."
    )


@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_sem_atividades(
    mock_service
):

    db_mock = Mock()

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_atividades_por_funcional.return_value = []

    controller = controller_atividades_realizadas(
        db_mock
    )

    with pytest.raises(HTTPException) as erro:

        controller.buscar_por_funcional(
            1001
        )

    assert erro.value.status_code == 404

    assert (
        erro.value.detail
        == "Nenhuma atividade encontrada para este funcional."
    )


@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_erro_interno(
    mock_service
):

    db_mock = Mock()

    instancia_service = mock_service.return_value

    instancia_service.get_recupera_atividades_por_funcional.side_effect = (
        Exception("Erro banco")
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    with pytest.raises(HTTPException) as erro:

        controller.buscar_por_funcional(
            1001
        )

    assert erro.value.status_code == 500

    assert (
        "Erro interno ao consultar funcional"
        in erro.value.detail
    )


# ==========================================
# cadastrar_atividade
# ==========================================

@patch(
    "src.contollers.atividades_realizadas.service_validacao_atividade"
)
@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_cadastrar_atividade_sucesso(
    mock_service,
    mock_validacao
):

    db_mock = Mock()

    payload_mock = {
        "funcional": 1001,
        "descricao": "Corrida"
    }

    atividade_mock = {
        "id": 1,
        "descricao": "Corrida"
    }

    instancia_service = mock_service.return_value

    instancia_service.salvar.return_value = (
        atividade_mock
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    response = controller.cadastrar_atividade(
        payload_mock
    )

    assert response == atividade_mock


@patch(
    "src.contollers.atividades_realizadas.service_validacao_atividade"
)
def test_cadastrar_atividade_erro_validacao(
    mock_validacao
):

    db_mock = Mock()

    payload_mock = {}

    instancia_validacao = mock_validacao.return_value

    instancia_validacao.validar.side_effect = (
        HTTPException(
            status_code=400,
            detail="Payload inválido"
        )
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    with pytest.raises(HTTPException) as erro:

        controller.cadastrar_atividade(
            payload_mock
        )

    assert erro.value.status_code == 400


@patch(
    "src.contollers.atividades_realizadas.service_validacao_atividade"
)
@patch(
    "src.contollers.atividades_realizadas.service_atividades_realizadas"
)
def test_cadastrar_atividade_erro_interno(
    mock_service,
    mock_validacao
):

    db_mock = Mock()

    payload_mock = {
        "funcional": 1001
    }

    instancia_service = mock_service.return_value

    instancia_service.salvar.side_effect = (
        Exception("Erro banco")
    )

    controller = controller_atividades_realizadas(
        db_mock
    )

    with pytest.raises(HTTPException) as erro:

        controller.cadastrar_atividade(
            payload_mock
        )

    assert erro.value.status_code == 500

    assert (
        "Erro interno ao cadastrar atividade"
        in erro.value.detail
    )