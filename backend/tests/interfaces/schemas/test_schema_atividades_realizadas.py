# tests/interfaces/test_schema_atividades_realizadas.py

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.interfaces.schemas.schema_atividaddes_realizadas import (
    AtividadeResponseSchema,
    AnaliseIATaskSchema,
    AtividadesPraticadasResponseSchema,
    CadastroAtividadeResponseSchema,
    AtividadeCriacaoSchema
)


# ==========================================
# ATIVIDADE RESPONSE
# ==========================================
def test_atividade_response_schema_success():

    data = {
        "funcional": 1,
        "codigo_atividade": "SUPINO-001",
        "nome_atividade": "Supino reto",
        "data_hora": datetime.now()
    }

    schema = AtividadeResponseSchema(
        **data
    )

    assert schema.funcional == 1

    assert (
        schema.codigo_atividade
        == "SUPINO-001"
    )

    assert (
        schema.nome_atividade
        == "Supino reto"
    )


def test_atividade_response_schema_missing_field():

    with pytest.raises(
        ValidationError
    ):

        AtividadeResponseSchema(
            funcional=1,
            nome_atividade="Supino"
        )


# ==========================================
# ANALISE IA TASK
# ==========================================
def test_analise_ia_task_schema_success():

    schema = AnaliseIATaskSchema(
        task_id="abc123",
        status="processando",
        endpoint_consulta=(
            "/analise-ia/analise/abc123"
        )
    )

    assert (
        schema.task_id
        == "abc123"
    )

    assert (
        schema.status
        == "processando"
    )


def test_analise_ia_task_schema_missing_field():

    with pytest.raises(
        ValidationError
    ):

        AnaliseIATaskSchema(
            task_id="abc123"
        )


# ==========================================
# ATIVIDADES PRATICADAS RESPONSE
# ==========================================
def test_atividades_praticadas_response_success():

    atividade = {
        "funcional": 1,
        "codigo_atividade": "SUPINO-001",
        "nome_atividade": "Supino reto",
        "data_hora": datetime.now()
    }

    analise = {
        "task_id": "abc123",
        "status": "processando",
        "endpoint_consulta": (
            "/analise-ia/analise/abc123"
        )
    }

    schema = (
        AtividadesPraticadasResponseSchema(
            atividades=[atividade],
            analise_ia=analise
        )
    )

    assert (
        len(schema.atividades)
        == 1
    )

    assert (
        schema.analise_ia.task_id
        == "abc123"
    )


def test_atividades_praticadas_response_invalid():

    with pytest.raises(
        ValidationError
    ):

        AtividadesPraticadasResponseSchema(
            atividades="errado",
            analise_ia={}
        )


# ==========================================
# CADASTRO RESPONSE
# ==========================================
def test_cadastro_atividade_response_success():

    atividade = {
        "funcional": 1,
        "codigo_atividade": "SUPINO-001",
        "nome_atividade": "Supino reto",
        "data_hora": datetime.now()
    }

    schema = (
        CadastroAtividadeResponseSchema(
            status="ok",
            atividade=atividade
        )
    )

    assert (
        schema.status
        == "ok"
    )

    assert (
        schema.atividade.codigo_atividade
        == "SUPINO-001"
    )


def test_cadastro_atividade_response_invalid():

    with pytest.raises(
        ValidationError
    ):

        CadastroAtividadeResponseSchema(
            status="ok"
        )


# ==========================================
# CREATE PAYLOAD
# ==========================================
def test_atividade_criacao_schema_success():

    schema = AtividadeCriacaoSchema(
        codigo_atividade="SUPINO-001",
        descricao="Treino de peito"
    )

    assert (
        schema.codigo_atividade
        == "SUPINO-001"
    )

    assert (
        schema.descricao
        == "Treino de peito"
    )


def test_atividade_criacao_schema_without_descricao():

    schema = AtividadeCriacaoSchema(
        codigo_atividade="SUPINO-001"
    )

    assert schema.descricao is None


def test_atividade_criacao_schema_codigo_vazio():

    with pytest.raises(
        ValidationError
    ):

        AtividadeCriacaoSchema(
            codigo_atividade=""
        )


def test_atividade_criacao_schema_missing_codigo():

    with pytest.raises(
        ValidationError
    ):

        AtividadeCriacaoSchema()


# ==========================================
# JSON SCHEMA / EXAMPLE
# ==========================================
def test_atividade_criacao_schema_example():

    schema = (
        AtividadeCriacaoSchema
        .model_json_schema()
    )

    example = (
        schema["example"]
    )

    assert (
        example["codigo_atividade"]
        == "SUPINO-001"
    )

    assert (
        example["descricao"]
        == "Treino de peito"
    )