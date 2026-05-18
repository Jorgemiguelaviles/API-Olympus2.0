from unittest.mock import MagicMock

from src.services.service_bancos.atividades_realizadas import (
    service_atividades_realizadas
)

from src.models.model_atividades import (
    model_atividades
)

from src.models.model_atividades_realizadas import (
    model_atividades_realizadas
)


# ==========================================
# Buscar todas atividades
# ==========================================
def test_get_recupera_todas_atividades():

    mock_db = MagicMock()

    retorno_mockado = [
        MagicMock(funcional=123),
        MagicMock(funcional=456)
    ]

    mock_db.query.return_value.all.return_value = (
        retorno_mockado
    )

    service = service_atividades_realizadas(
        mock_db
    )

    resultado = (
        service.get_recupera_todas_atividades()
    )

    mock_db.query.assert_called_once_with(
        model_atividades_realizadas
    )

    assert resultado == retorno_mockado


# ==========================================
# Buscar por funcional
# ==========================================
def test_get_recupera_atividades_por_funcional():

    mock_db = MagicMock()

    retorno_mockado = [
        MagicMock(funcional=123456789)
    ]

    query_mock = MagicMock()

    mock_db.query.return_value = (
        query_mock
    )

    query_mock.filter.return_value.all.return_value = (
        retorno_mockado
    )

    service = service_atividades_realizadas(
        mock_db
    )

    resultado = (
        service.get_recupera_atividades_por_funcional(
            123456789
        )
    )

    mock_db.query.assert_called_once_with(
        model_atividades_realizadas
    )

    query_mock.filter.assert_called_once()

    assert resultado == retorno_mockado


# ==========================================
# Salvar com sucesso
# ==========================================
def test_salvar_atividade_com_sucesso():

    mock_db = MagicMock()

    atividade_existente = MagicMock(
        codigo_atividade=1
    )

    query_mock = MagicMock()

    mock_db.query.return_value = (
        query_mock
    )

    query_mock.filter.return_value.first.return_value = (
        atividade_existente
    )

    payload = {
        "funcional": 123456789,
        "codigo_atividade": "Corrida",
        "descricao": "Treino",
        "data_hora": "2026-05-17"
    }

    service = service_atividades_realizadas(
        mock_db
    )

    resultado = service.salvar(
        payload
    )

    mock_db.add.assert_called_once()

    mock_db.commit.assert_called_once()

    mock_db.refresh.assert_called_once()

    assert isinstance(
        resultado,
        model_atividades_realizadas
    )


# ==========================================
# Salvar atividade inexistente
# ==========================================
def test_salvar_atividade_inexistente():

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

    service = service_atividades_realizadas(
        mock_db
    )

    try:

        service.salvar(
            payload
        )

        assert False

    except ValueError as erro:

        assert str(erro) == (
            "Atividade não encontrada."
        )

    mock_db.add.assert_not_called()

    mock_db.commit.assert_not_called()