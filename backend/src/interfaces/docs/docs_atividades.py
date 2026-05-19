# src/interfaces/docs/docs_atividades.py

from src.interfaces.schemas.schema_atividades import (
    AtividadeOpcaoResponseSchema
)

DOC_CADASTRAR_OPCAO_ATIVIDADE = {

    "response_model": AtividadeOpcaoResponseSchema,

    "summary": "Cadastrar atividade",

    "description": (
        "Cadastra uma nova atividade disponível no sistema."
    ),

    "responses": {

        201: {
            "description": "Atividade cadastrada com sucesso."
        },

        400: {
            "description": "Dados inválidos."
        },

        409: {
            "description": "Atividade já cadastrada."
        },

        500: {
            "description": "Erro interno."
        }
    }
}