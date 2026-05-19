# src/interfaces/docs/docs_atividades.py

from typing import List

from src.interfaces.schemas.schema_atividades import (
    AtividadeRespostaSchema,
    AtividadeComAnaliseSchema
)


# ==========================================
# DOC CADASTRAR
# ==========================================

DOC_CADASTRAR_ATIVIDADE = {

    "response_model": AtividadeRespostaSchema,

    "summary": "Cadastrar atividade realizada",

    "description": (
        "Cria um novo registro de atividade física realizada."
    ),

    "responses": {

        201: {
            "description": "Atividade cadastrada com sucesso."
        },

        400: {
            "description": "Dados inválidos."
        },

        404: {
            "description": "Atividade não encontrada."
        },

        500: {
            "description": "Erro interno."
        }
    }
}


# ==========================================
# DOC BUSCAR POR FUNCIONAL
# ==========================================

DOC_BUSCAR_POR_FUNCIONAL = {

    "response_model": AtividadeComAnaliseSchema,

    "summary": "Buscar atividades por funcional",

    "description": (
        "Retorna todas as atividades vinculadas ao funcional."
    ),

    "responses": {

        200: {
            "description": "Atividades encontradas."
        },

        404: {
            "description": "Nenhuma atividade encontrada."
        },

        500: {
            "description": "Erro interno."
        }
    }
}


# ==========================================
# DOC BUSCAR TODAS
# ==========================================

DOC_BUSCAR_TODAS = {

    "response_model": List[AtividadeRespostaSchema],

    "summary": "Buscar todas as atividades",

    "description": (
        "Retorna todas as atividades físicas registradas."
    ),

    "responses": {

        200: {
            "description": "Lista retornada com sucesso."
        },

        404: {
            "description": "Nenhuma atividade encontrada."
        },

        500: {
            "description": "Erro interno."
        }
    }
}