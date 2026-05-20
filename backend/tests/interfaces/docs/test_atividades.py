# tests/interfaces/docs/test_docs_atividades.py

from typing import List

from src.interfaces.docs.docs_atividades import (
    DOC_BUSCAR_OPCOES_ATIVIDADES,
    DOC_CADASTRAR_OPCAO_ATIVIDADE
)

from src.interfaces.schemas.schema_atividades import (
    AtividadeExistenteResponseSchema,
    AtividadeOpcaoResponseSchema
)


# ==========================================
# TESTE DOC BUSCAR OPÇÕES
# ==========================================
def test_doc_buscar_opcoes_response_model():

    assert (
        DOC_BUSCAR_OPCOES_ATIVIDADES["response_model"]
        == List[AtividadeExistenteResponseSchema]
    )


def test_doc_buscar_opcoes_summary():

    assert (
        DOC_BUSCAR_OPCOES_ATIVIDADES["summary"]
        == "Buscar atividades disponíveis"
    )


def test_doc_buscar_opcoes_description():

    assert (
        "disponíveis para seleção"
        in DOC_BUSCAR_OPCOES_ATIVIDADES["description"]
    )


def test_doc_buscar_opcoes_responses():

    responses = DOC_BUSCAR_OPCOES_ATIVIDADES["responses"]

    assert 200 in responses
    assert 404 in responses
    assert 500 in responses


def test_doc_buscar_opcoes_response_descriptions():

    responses = DOC_BUSCAR_OPCOES_ATIVIDADES["responses"]

    assert (
        responses[200]["description"]
        == "Atividades recuperadas com sucesso."
    )

    assert (
        responses[404]["description"]
        == "Nenhuma atividade encontrada."
    )

    assert (
        responses[500]["description"]
        == "Erro interno do servidor."
    )


# ==========================================
# TESTE DOC CADASTRAR OPÇÃO
# ==========================================
def test_doc_cadastrar_opcao_response_model():

    assert (
        DOC_CADASTRAR_OPCAO_ATIVIDADE["response_model"]
        == AtividadeOpcaoResponseSchema
    )


def test_doc_cadastrar_opcao_summary():

    assert (
        DOC_CADASTRAR_OPCAO_ATIVIDADE["summary"]
        == "Cadastrar atividade"
    )


def test_doc_cadastrar_opcao_description():

    assert (
        "disponível no sistema"
        in DOC_CADASTRAR_OPCAO_ATIVIDADE["description"]
    )


def test_doc_cadastrar_opcao_responses():

    responses = DOC_CADASTRAR_OPCAO_ATIVIDADE["responses"]

    assert 201 in responses
    assert 400 in responses
    assert 409 in responses
    assert 500 in responses


def test_doc_cadastrar_opcao_response_descriptions():

    responses = DOC_CADASTRAR_OPCAO_ATIVIDADE["responses"]

    assert (
        responses[201]["description"]
        == "Atividade cadastrada com sucesso."
    )

    assert (
        responses[400]["description"]
        == "Dados inválidos."
    )

    assert (
        responses[409]["description"]
        == "Atividade já cadastrada."
    )

    assert (
        responses[500]["description"]
        == "Erro interno."
    )