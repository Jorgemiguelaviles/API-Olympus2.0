from typing import List

from src.interfaces.schemas.schema_atividades import (
    AtividadeExistenteResponseSchema,
    AtividadeOpcaoResponseSchema
)


# ==========================================
# DOC - BUSCAR OPÇÕES
# ==========================================
DOC_BUSCAR_OPCOES_ATIVIDADES = {

    "response_model": List[AtividadeExistenteResponseSchema],

    "summary": "Buscar atividades disponíveis",

    "description": (
        "Retorna todas as atividades físicas "
        "disponíveis para seleção."
    ),

    "responses": {

        200: {
            "description": "Atividades recuperadas com sucesso."
        },

        404: {
            "description": "Nenhuma atividade encontrada."
        },

        500: {
            "description": "Erro interno do servidor."
        }
    }
}


# ==========================================
# DOC - CADASTRAR OPÇÃO
# ==========================================
DOC_CADASTRAR_OPCAO_ATIVIDADE = {

    "response_model": AtividadeOpcaoResponseSchema,

    "summary": "Cadastrar atividade",

    "description": (
        "Cadastra uma nova atividade "
        "disponível no sistema."
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