# tests/interfaces/docs/test_docs_atividades_realizadas.py

from fastapi import status

from src.interfaces.docs.docs_atividades_realizadas import (
    DOC_CADASTRAR_ATIVIDADE,
    DOC_BUSCAR_POR_FUNCIONAL,
    DOC_BUSCAR_TODAS
)

from src.interfaces.schemas.schema_atividaddes_realizadas import (
    CadastroAtividadeResponseSchema,
    AtividadesPraticadasResponseSchema,
    AtividadeResponseSchema
)


# ==========================================
# DOC CADASTRAR ATIVIDADE
# ==========================================
def test_doc_cadastrar_atividade():

    assert (
        DOC_CADASTRAR_ATIVIDADE["response_model"]
        == CadastroAtividadeResponseSchema
    )

    assert (
        DOC_CADASTRAR_ATIVIDADE["summary"]
        == "Cadastrar atividade realizada"
    )

    assert (
        DOC_CADASTRAR_ATIVIDADE["status_code"]
        == status.HTTP_201_CREATED
    )

    responses = DOC_CADASTRAR_ATIVIDADE["responses"]

    assert status.HTTP_201_CREATED in responses
    assert status.HTTP_400_BAD_REQUEST in responses
    assert status.HTTP_404_NOT_FOUND in responses
    assert status.HTTP_500_INTERNAL_SERVER_ERROR in responses


# ==========================================
# DOC BUSCAR POR FUNCIONAL
# ==========================================
def test_doc_buscar_por_funcional():

    assert (
        DOC_BUSCAR_POR_FUNCIONAL["response_model"]
        == AtividadesPraticadasResponseSchema
    )

    assert (
        DOC_BUSCAR_POR_FUNCIONAL["summary"]
        == "Buscar minhas atividades"
    )

    responses = DOC_BUSCAR_POR_FUNCIONAL["responses"]

    assert status.HTTP_200_OK in responses
    assert status.HTTP_404_NOT_FOUND in responses
    assert status.HTTP_500_INTERNAL_SERVER_ERROR in responses


# ==========================================
# DOC BUSCAR TODAS
# ==========================================
def test_doc_buscar_todas():

    response_model = (
        DOC_BUSCAR_TODAS["response_model"]
    )

    assert response_model is not None

    assert (
        DOC_BUSCAR_TODAS["summary"]
        == "Buscar todas as atividades"
    )

    responses = DOC_BUSCAR_TODAS["responses"]

    assert status.HTTP_200_OK in responses
    assert status.HTTP_404_NOT_FOUND in responses
    assert status.HTTP_500_INTERNAL_SERVER_ERROR in responses


# ==========================================
# DESCRIPTION EXISTS
# ==========================================
def test_all_docs_have_description():

    docs = [
        DOC_CADASTRAR_ATIVIDADE,
        DOC_BUSCAR_POR_FUNCIONAL,
        DOC_BUSCAR_TODAS
    ]

    for doc in docs:

        assert "description" in doc

        assert isinstance(
            doc["description"],
            str
        )

        assert len(doc["description"]) > 0


# ==========================================
# RESPONSES HAVE DESCRIPTION
# ==========================================
def test_all_responses_have_description():

    docs = [
        DOC_CADASTRAR_ATIVIDADE,
        DOC_BUSCAR_POR_FUNCIONAL,
        DOC_BUSCAR_TODAS
    ]

    for doc in docs:

        responses = doc["responses"]

        for _, response in responses.items():

            assert "description" in response

            assert isinstance(
                response["description"],
                str
            )

            assert len(
                response["description"]
            ) > 0