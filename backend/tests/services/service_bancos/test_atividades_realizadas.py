# tests/services/test_service_atividades_realizadas.py

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.services.service_bancos.atividades_realizadas import (
    service_atividades_realizadas
)


# ==========================================
# FIXTURE
# ==========================================
@pytest.fixture
def fake_db():
    return MagicMock()


@pytest.fixture
def service(fake_db):
    return service_atividades_realizadas(fake_db)


# ==========================================
# GET TODAS ATIVIDADES
# ==========================================
def test_get_recupera_todas_atividades(service, fake_db):

    atividade1 = MagicMock()
    atividade2 = MagicMock()

    fake_db.query.return_value.all.return_value = [
        atividade1,
        atividade2
    ]

    resultado = service.get_recupera_todas_atividades()

    assert resultado == [atividade1, atividade2]

    fake_db.query.assert_called_once()


# ==========================================
# GET POR FUNCIONAL
# ==========================================
def test_get_recupera_atividades_por_funcional(
    service,
    fake_db
):

    atividade = MagicMock()

    atividade.funcional = 1
    atividade.codigo_atividade = "SUPINO-001"
    atividade.descricao = "Treino peito"
    atividade.data_hora = datetime.now()

    (
        fake_db.query.return_value
        .filter.return_value
        .all.return_value
    ) = [atividade]

    resultado = service.get_recupera_atividades_por_funcional(1)

    assert resultado == [
        {
            "funcional": 1,
            "codigo_atividade": "SUPINO-001",
            "descricao": "Treino peito",
            "data_hora": atividade.data_hora
        }
    ]

    fake_db.query.assert_called_once()


# ==========================================
# SALVAR SUCESSO
# ==========================================
def test_salvar_sucesso(
    service,
    fake_db
):

    atividade_existente = MagicMock()
    atividade_existente.codigo_atividade = "SUPINO-001"

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = atividade_existente

    payload = {
        "funcional": 1,
        "codigo_atividade": "SUPINO-001",
        "descricao": "Treino peito",
        "data_hora": datetime.now()
    }

    resultado = service.salvar(payload)

    assert resultado is not None

    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()


# ==========================================
# SALVAR - ATIVIDADE NÃO EXISTE
# ==========================================
def test_salvar_atividade_nao_encontrada(
    service,
    fake_db
):

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = None

    payload = {
        "funcional": 1,
        "codigo_atividade": "INEXISTENTE",
        "descricao": "Teste",
        "data_hora": datetime.now()
    }

    with pytest.raises(ValueError) as erro:

        service.salvar(payload)

    assert str(erro.value) == "Atividade não encontrada."


# ==========================================
# SALVAR - ERRO NO COMMIT
# ==========================================
def test_salvar_commit_error(
    service,
    fake_db
):

    atividade_existente = MagicMock()
    atividade_existente.codigo_atividade = "SUPINO-001"

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = atividade_existente

    fake_db.commit.side_effect = Exception(
        "Erro banco"
    )

    payload = {
        "funcional": 1,
        "codigo_atividade": "SUPINO-001",
        "descricao": "Teste",
        "data_hora": datetime.now()
    }

    with pytest.raises(Exception):

        service.salvar(payload)