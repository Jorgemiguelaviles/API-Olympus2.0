from datetime import datetime

import pytest
from pydantic import ValidationError

from backend.src.interfaces.schemas.schema_atividades import (
    AtividadeCriacaoSchema,
    AtividadeRespostaSchema,
    AtividadeExistenteResponseSchema
)


# ====================================================
# AtividadeCriacaoSchema
# ====================================================

def test_criacao_schema_valido():

    payload = AtividadeCriacaoSchema(
        funcional=123456789,
        codigo_atividade="RUN",
        descricao="Corrida"
    )

    assert payload.funcional == 123456789
    assert payload.codigo_atividade == "RUN"
    assert payload.descricao == "Corrida"


def test_criacao_schema_sem_descricao():

    payload = AtividadeCriacaoSchema(
        funcional=123456789,
        codigo_atividade="RUN"
    )

    assert payload.descricao is None


def test_criacao_schema_sem_funcional():

    with pytest.raises(
        ValidationError
    ):

        AtividadeCriacaoSchema(
            codigo_atividade="RUN"
        )


def test_criacao_schema_tipo_invalido():

    with pytest.raises(
        ValidationError
    ):

        AtividadeCriacaoSchema(
            funcional="abc",
            codigo_atividade="RUN"
        )


# ====================================================
# AtividadeRespostaSchema
# ====================================================

def test_resposta_schema_valido():

    now = datetime.now()

    payload = AtividadeRespostaSchema(
        funcional=123456789,
        codigo_atividade="RUN",
        descricao="Corrida",
        data_hora=now
    )

    assert payload.funcional == 123456789
    assert payload.codigo_atividade == "RUN"
    assert payload.data_hora == now


def test_resposta_schema_model_dump():

    now = datetime.now()

    payload = AtividadeRespostaSchema(
        funcional=123456789,
        codigo_atividade="RUN",
        descricao="Teste",
        data_hora=now
    )

    data = payload.model_dump()

    assert data["funcional"] == 123456789
    assert data["codigo_atividade"] == "RUN"


# ====================================================
# from_attributes
# ====================================================

class FakeAtividade:

    funcional = 123456789
    codigo_atividade = "RUN"
    descricao = "Corrida"
    data_hora = datetime.now()


def test_resposta_schema_from_attributes():

    obj = FakeAtividade()

    schema = AtividadeRespostaSchema.model_validate(
        obj
    )

    assert schema.funcional == 123456789
    assert schema.codigo_atividade == "RUN"


# ====================================================
# AtividadeExistenteResponseSchema
# ====================================================

def test_atividade_existente_schema():

    payload = AtividadeExistenteResponseSchema(
        codigo_atividade="RUN",
        nome_atividade="Corrida"
    )

    assert payload.codigo_atividade == "RUN"
    assert payload.nome_atividade == "Corrida"


def test_atividade_existente_schema_campo_obrigatorio():

    with pytest.raises(
        ValidationError
    ):

        AtividadeExistenteResponseSchema(
            codigo_atividade="RUN"
        )


class FakeAtividadeExistente:

    codigo_atividade = "RUN"
    nome_atividade = "Corrida"


def test_atividade_existente_from_attributes():

    obj = FakeAtividadeExistente()

    schema = (
        AtividadeExistenteResponseSchema
        .model_validate(obj)
    )

    assert schema.codigo_atividade == "RUN"
    assert schema.nome_atividade == "Corrida"