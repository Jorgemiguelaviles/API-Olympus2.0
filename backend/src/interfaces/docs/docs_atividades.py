# src/interfaces/docs/docs_atividades.py

from typing import List

from src.interfaces.schemas.schema_atividades import (
    AtividadeRespostaSchema,
    AtividadeComAnaliseSchema
)

# ==========================================
# POST - cadastrar atividade
# ==========================================

DOC_CADASTRAR_ATIVIDADE = {
    "response_model": AtividadeRespostaSchema,
    "summary": "Cadastrar atividade realizada",
    "description": "Cria um novo registro de atividade física realizada.",
    "responses": {
        201: {
            "description": "Atividade cadastrada com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "funcional": 123456789,
                        "codigo_atividade": "uuid-atividade",
                        "descricao": "Treino de peito",
                        "data_hora": "2026-05-17T14:30:00"
                    }
                }
            }
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
# GET - buscar por funcional
# ==========================================

DOC_BUSCAR_POR_FUNCIONAL = {
    "response_model": AtividadeComAnaliseSchema,
    "summary": "Buscar atividades por funcional",
    "description": "Retorna todas as atividades vinculadas a um funcional.",
    "responses": {
        200: {
            "description": "Atividades encontradas com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "atividades": [
                            {
                                "funcional": 123456789,
                                "codigo_atividade": "uuid-atividade",
                                "descricao": "Treino de peito",
                                "data_hora": "2026-05-17T14:30:00"
                            }
                        ],
                        "analise_ia": "Análise gerada pela IA."
                    }
                }
            }
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
# GET - buscar todas
# ==========================================

DOC_BUSCAR_TODAS = {
    "response_model": List[AtividadeRespostaSchema],
    "summary": "Buscar todas as atividades realizadas",
    "description": "Retorna todas as atividades físicas registradas.",
    "responses": {
        200: {
            "description": "Lista recuperada com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "funcional": 123456789,
                            "codigo_atividade": "uuid-atividade",
                            "descricao": "Treino de peito",
                            "data_hora": "2026-05-17T14:30:00"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Nenhuma atividade encontrada."
        }
    }
}