from typing import List

from fastapi import status

from src.interfaces.schemas.schema_atividaddes_realizadas import (
    CadastroAtividadeResponseSchema,
    AtividadesPraticadasResponseSchema,
    AtividadeResponseSchema
)


# ==========================================
# CADASTRAR ATIVIDADE
# ==========================================
DOC_CADASTRAR_ATIVIDADE = {

    "response_model": CadastroAtividadeResponseSchema,

    "summary": "Cadastrar atividade realizada",

    "description": (
        "Cria um novo registro de atividade física."
    ),

    "status_code": status.HTTP_201_CREATED,

    "responses": {

        status.HTTP_201_CREATED: {
            "description": "Atividade cadastrada com sucesso."
        },

        status.HTTP_400_BAD_REQUEST: {
            "description": "Dados inválidos."
        },

        status.HTTP_404_NOT_FOUND: {
            "description": "Atividade não encontrada."
        },

        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro interno."
        }
    }
}


# ==========================================
# BUSCAR POR FUNCIONAL
# ==========================================
DOC_BUSCAR_POR_FUNCIONAL = {

    "response_model": AtividadesPraticadasResponseSchema,

    "summary": "Buscar minhas atividades",

    "description": (
        "Retorna todas as atividades do usuário autenticado."
    ),

    "responses": {

        status.HTTP_200_OK: {
            "description": "Atividades encontradas."
        },

        status.HTTP_404_NOT_FOUND: {
            "description": "Nenhuma atividade encontrada."
        },

        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro interno."
        }
    }
}


# ==========================================
# BUSCAR TODAS
# ==========================================
DOC_BUSCAR_TODAS = {

    "response_model": List[AtividadeResponseSchema],

    "summary": "Buscar todas as atividades",

    "description": (
        "Retorna todas as atividades registradas."
    ),

    "responses": {

        status.HTTP_200_OK: {
            "description": "Lista retornada com sucesso."
        },

        status.HTTP_404_NOT_FOUND: {
            "description": "Nenhuma atividade encontrada."
        },

        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro interno."
        }
    }
}