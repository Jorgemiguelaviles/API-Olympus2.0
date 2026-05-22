from fastapi import status

from src.interfaces.schemas.schemas_analise_ia import (
    StatusAnaliseIAResponseSchema
)


# ==========================================
# STATUS DA ANÁLISE IA
# ==========================================
DOC_STATUS_ANALISE_IA = {

    "response_model": StatusAnaliseIAResponseSchema,

    "summary": "Consultar status da análise IA",

    "description": (
        "Consulta o status da análise assíncrona "
        "gerada pela IA com base nas atividades "
        "físicas do usuário."
    ),

    "responses": {

        status.HTTP_200_OK: {
            "description": (
                "Status da análise retornado com sucesso."
            )
        },

        status.HTTP_404_NOT_FOUND: {
            "description": (
                "Task da análise não encontrada."
            )
        },

        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": (
                "Erro interno ao consultar análise."
            )
        }
    }
}