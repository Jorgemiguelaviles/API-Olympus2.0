# tests/services/test_service_atividades.py

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from src.services.service_bancos.atividades_existentes import (
    service_atividades
)


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def fake_db():
    return MagicMock()


@pytest.fixture
def service(fake_db):
    return service_atividades(fake_db)


# ==========================================
# CADASTRAR ATIVIDADE - SUCESSO
# ==========================================
def test_cadastrar_atividade_sucesso(
    service,
    fake_db
):

    payload = {
        "descricao": "Musculação"
    }

    resultado = service.cadastrar_atividade(
        payload
    )

    assert resultado is not None

    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()


# ==========================================
# CADASTRAR ATIVIDADE - ERRO
# ==========================================
def test_cadastrar_atividade_erro(
    service,
    fake_db
):

    fake_db.commit.side_effect = Exception(
        "Erro banco"
    )

    payload = {
        "descricao": "Natação"
    }

    with pytest.raises(HTTPException) as erro:

        service.cadastrar_atividade(
            payload
        )

    assert erro.value.status_code == 500

    assert (
        "Erro ao cadastrar atividade"
        in erro.value.detail
    )

    fake_db.rollback.assert_called_once()


# ==========================================
# BUSCAR TODAS ATIVIDADES
# ==========================================
def test_buscar_todas_atividades(
    service,
    fake_db
):

    atividade1 = MagicMock()
    atividade2 = MagicMock()

    fake_db.query.return_value.all.return_value = [
        atividade1,
        atividade2
    ]

    resultado = service.buscar_todas_atividades()

    assert resultado == [
        atividade1,
        atividade2
    ]

    fake_db.query.assert_called_once()


# ==========================================
# BUSCAR TODAS - LISTA VAZIA
# ==========================================
def test_buscar_todas_atividades_vazio(
    service,
    fake_db
):

    fake_db.query.return_value.all.return_value = []

    resultado = service.buscar_todas_atividades()

    assert resultado == []