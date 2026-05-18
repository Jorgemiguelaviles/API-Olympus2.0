from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from src.services.validadores.valida_atividades_realizadas import (
    service_validacao_atividade
)

from src.models.model_atividades import (
    model_atividades
)


# ==========================================
# Validação com sucesso
# ==========================================
def test_validacao_com_sucesso():

    mock_db = MagicMock()

    atividade_mock = MagicMock(
        codigo_atividade=1,
        nome_atividade="Corrida"
    )

    query_mock = MagicMock()

    mock_db.query.return_value = (
        query_mock
    )

    query_mock.filter.return_value.first.return_value = (
        atividade_mock
    )

    payload = {
        "funcional": 123456789,
        "codigo_atividade": "Corrida"
    }

    service = (
        service_validacao_atividade()
    )

    resultado = service.validar(
        payload,
        mock_db
    )

    mock_db.query.assert_called_once_with(
        model_atividades
    )

    assert resultado == (
        atividade_mock
    )


# ==========================================
# Funcional inválido
# ==========================================
def test_funcional_invalido():

    mock_db = MagicMock()

    payload = {
        "funcional": 12345,
        "codigo_atividade": "Corrida"
    }

    service = (
        service_validacao_atividade()
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        service.validar(
            payload,
            mock_db
        )

    assert (
        erro.value.status_code
        == 400
    )

    assert (
        erro.value.detail
        == "Funcional deve conter exatamente 9 números."
    )

    mock_db.query.assert_not_called()


# ==========================================
# Atividade inexistente
# ==========================================
def test_atividade_nao_existe():

    mock_db = MagicMock()

    query_mock = MagicMock()

    mock_db.query.return_value = (
        query_mock
    )

    query_mock.filter.return_value.first.return_value = (
        None
    )

    payload = {
        "funcional": 123456789,
        "codigo_atividade": "AtividadeFake"
    }

    service = (
        service_validacao_atividade()
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        service.validar(
            payload,
            mock_db
        )

    assert (
        erro.value.status_code
        == 404
    )

    assert (
        erro.value.detail
        == "Atividade informada não existe."
    )