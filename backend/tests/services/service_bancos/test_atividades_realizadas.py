from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.services.service_bancos.atividades_realizadas import (
    service_atividades_realizadas
)


# ==========================================
# Mock da model atividade realizada
# ==========================================

class MockAtividadeRealizada:

    def __init__(
        self,
        funcional,
        codigo_atividade,
        descricao,
        data_hora
    ):
        self.funcional = funcional
        self.codigo_atividade = codigo_atividade
        self.descricao = descricao
        self.data_hora = data_hora


# ==========================================
# Mock da model atividade
# ==========================================

class MockAtividade:

    def __init__(
        self,
        codigo_atividade,
        nome_atividade
    ):
        self.codigo_atividade = codigo_atividade
        self.nome_atividade = nome_atividade


# ==========================================
# Fixture banco fake
# ==========================================

@pytest.fixture
def mock_db():

    return MagicMock()


# ==========================================
# Teste buscar todas atividades
# ==========================================

def test_get_recupera_todas_atividades(
    mock_db
):

    atividades_mock = [
        MockAtividadeRealizada(
            funcional=1001,
            codigo_atividade="RUN",
            descricao="Corrida",
            data_hora=datetime.now()
        ),
        MockAtividadeRealizada(
            funcional=1002,
            codigo_atividade="SWIM",
            descricao="Natação",
            data_hora=datetime.now()
        )
    ]

    mock_db.query.return_value.all.return_value = (
        atividades_mock
    )

    service = service_atividades_realizadas(
        mock_db
    )

    resultado = service.get_recupera_todas_atividades()

    assert resultado == atividades_mock

    mock_db.query.assert_called_once()


# ==========================================
# Teste buscar atividades por funcional
# ==========================================

def test_get_recupera_atividades_por_funcional(
    mock_db
):

    atividades_mock = [
        MockAtividadeRealizada(
            funcional=1001,
            codigo_atividade="RUN",
            descricao="Corrida de 5km",
            data_hora=datetime.now()
        )
    ]

    (
        mock_db.query.return_value
        .filter.return_value
        .all.return_value
    ) = atividades_mock

    service = service_atividades_realizadas(
        mock_db
    )

    resultado = (
        service.get_recupera_atividades_por_funcional(
            1001
        )
    )

    assert len(resultado) == 1

    assert resultado[0]["funcional"] == 1001

    assert resultado[0]["codigo_atividade"] == "RUN"

    assert resultado[0]["descricao"] == "Corrida de 5km"


# ==========================================
# Teste buscar atividades por funcional vazio
# ==========================================

def test_get_recupera_atividades_por_funcional_vazio(
    mock_db
):

    (
        mock_db.query.return_value
        .filter.return_value
        .all.return_value
    ) = []

    service = service_atividades_realizadas(
        mock_db
    )

    resultado = (
        service.get_recupera_atividades_por_funcional(
            9999
        )
    )

    assert resultado == []


# ==========================================
# Teste salvar atividade com sucesso
# ==========================================

def test_salvar_atividade_sucesso(
    mock_db
):

    atividade_existente = MockAtividade(
        codigo_atividade="RUN",
        nome_atividade="Corrida"
    )

    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = atividade_existente

    service = service_atividades_realizadas(
        mock_db
    )

    payload = {
        "funcional": 1001,
        "codigo_atividade": "Corrida",
        "descricao": "Corrida no parque",
        "data_hora": datetime.now()
    }

    resultado = service.salvar(
        payload
    )

    assert resultado.funcional == 1001

    assert resultado.codigo_atividade == "RUN"

    assert resultado.descricao == "Corrida no parque"

    mock_db.add.assert_called_once()

    mock_db.commit.assert_called_once()

    mock_db.refresh.assert_called_once()


# ==========================================
# Teste salvar atividade inexistente
# ==========================================

def test_salvar_atividade_inexistente(
    mock_db
):

    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = None

    service = service_atividades_realizadas(
        mock_db
    )

    payload = {
        "funcional": 1001,
        "codigo_atividade": "AtividadeFake",
        "descricao": "Teste",
        "data_hora": datetime.now()
    }

    with pytest.raises(
        ValueError,
        match="Atividade não encontrada."
    ):

        service.salvar(
            payload
        )


# ==========================================
# Teste salvar chama métodos do banco
# ==========================================

def test_salvar_chama_metodos_db(
    mock_db
):

    atividade_existente = MockAtividade(
        codigo_atividade="SWIM",
        nome_atividade="Natação"
    )

    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = atividade_existente

    service = service_atividades_realizadas(
        mock_db
    )

    payload = {
        "funcional": 2001,
        "codigo_atividade": "Natação",
        "descricao": "Treino de natação",
        "data_hora": datetime.now()
    }

    service.salvar(
        payload
    )

    assert mock_db.add.called

    assert mock_db.commit.called

    assert mock_db.refresh.called