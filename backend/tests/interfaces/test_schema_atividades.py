# tests/interfaces/test_schema_atividades.py

import pytest
from pydantic import ValidationError

from src.interfaces.schemas.schema_atividades import (
    AtividadeExistenteResponseSchema,
    AtividadeCriacaoOpcaoSchema,
    AtividadeOpcaoResponseSchema
)


# ==========================================
# ATIVIDADE EXISTENTE RESPONSE
# ==========================================
def test_atividade_existente_response_schema_success():

    schema = AtividadeExistenteResponseSchema(
        codigo_atividade="musculacao-001",
        nome_atividade="Musculação"
    )

    assert schema.codigo_atividade == "musculacao-001"
    assert schema.nome_atividade == "Musculação"


def test_atividade_existente_response_schema_missing_fields():

    with pytest.raises(ValidationError):

        AtividadeExistenteResponseSchema(
            codigo_atividade="musculacao-001"
        )


def test_atividade_existente_response_schema_json_schema():

    schema = AtividadeExistenteResponseSchema.model_json_schema()

    properties = schema["properties"]

    assert properties["codigo_atividade"]["example"] == "musculacao-001"
    assert properties["nome_atividade"]["example"] == "Musculação"


# ==========================================
# ATIVIDADE CRIACAO OPCAO
# ==========================================
def test_atividade_criacao_opcao_schema_success():

    schema = AtividadeCriacaoOpcaoSchema(
        descricao="Natação"
    )

    assert schema.descricao == "Natação"


def test_atividade_criacao_opcao_schema_min_length():

    with pytest.raises(ValidationError):

        AtividadeCriacaoOpcaoSchema(
            descricao="AB"
        )


def test_atividade_criacao_opcao_schema_missing_field():

    with pytest.raises(ValidationError):

        AtividadeCriacaoOpcaoSchema()


def test_atividade_criacao_opcao_schema_json_schema():

    schema = AtividadeCriacaoOpcaoSchema.model_json_schema()

    properties = schema["properties"]

    assert properties["descricao"]["example"] == "Natação"


# ==========================================
# ATIVIDADE OPCAO RESPONSE
# ==========================================
def test_atividade_opcao_response_schema_success():

    schema = AtividadeOpcaoResponseSchema(
        codigo_atividade="natacao-001",
        nome_atividade="Natação"
    )

    assert schema.codigo_atividade == "natacao-001"
    assert schema.nome_atividade == "Natação"


def test_atividade_opcao_response_schema_missing_fields():

    with pytest.raises(ValidationError):

        AtividadeOpcaoResponseSchema(
            codigo_atividade="natacao-001"
        )


def test_atividade_opcao_response_schema_json_schema():

    schema = AtividadeOpcaoResponseSchema.model_json_schema()

    properties = schema["properties"]

    assert properties["codigo_atividade"]["example"] == "natacao-001"
    assert properties["nome_atividade"]["example"] == "Natação"