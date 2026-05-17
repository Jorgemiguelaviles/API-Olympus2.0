from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.schema_atividades import (
    AtividadeCriacaoSchema,
    AtividadeRespostaSchema
)

from src.contollers.atividades_realizadas import (
    controller_atividades_realizadas
)


roteador_atividades_praticadas = APIRouter(
    prefix="/atividades/praticadas",
    tags=["Atividades Praticadas"]
)


# ==========================================
# Cadastro de atividade realizada
# ==========================================

@roteador_atividades_praticadas.post(
    "/",
    response_model=AtividadeRespostaSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar atividade realizada",
    description="Cria um novo registro de atividade física realizada.",
    responses={
        201: {
            "description": "Atividade cadastrada com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "funcional": 123456789,
                        "codigo_atividade": 1,
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
            "description": "Erro interno ao consultar atividades."
        }
    }
)
def cadastrar_atividade(
    payload: AtividadeCriacaoSchema,
    db: Session = Depends(get_db)
):

    nova_atividade = {
        "funcional": payload.funcional,
        "codigo_atividade": payload.codigo_atividade,
        "descricao": payload.descricao,
        "data_hora": datetime.now()
    }

    controller_atividades_realizadas(
        db
    ).cadastrar_atividade(
        nova_atividade
    )

    return nova_atividade


# ==========================================
# Buscar atividades por funcional
# ==========================================

@roteador_atividades_praticadas.get(
    "/{funcional}",
    response_model=List[AtividadeRespostaSchema],
    summary="Buscar atividades por funcional",
    description="Retorna todas as atividades vinculadas a um funcional.",
    responses={
        200: {
            "description": "Atividades encontradas com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "funcional": 123456789,
                            "codigo_atividade": 1,
                            "descricao": "Treino de peito",
                            "data_hora": "2026-05-17T14:30:00"
                        },
                        {
                            "funcional": 123456789,
                            "codigo_atividade": 2,
                            "descricao": "Treino de perna",
                            "data_hora": "2026-05-17T18:00:00"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Nenhuma atividade encontrada."
        },
        500: {
            "description": "Erro interno ao consultar atividades."
        }
    }
)
def buscar_por_funcional(
    funcional: int = Path(
        ...,
        description="Código funcional com 9 dígitos.",
        example=123456789
    ),
    db: Session = Depends(get_db)
):

    return controller_atividades_realizadas(
        db
    ).buscar_por_funcional(
        funcional
    )


# ==========================================
# Buscar todas as atividades realizadas
# ==========================================

@roteador_atividades_praticadas.get(
    "/",
    response_model=List[AtividadeRespostaSchema],
    summary="Buscar todas as atividades realizadas",
    description="Retorna todas as atividades físicas registradas.",
    responses={
        200: {
            "description": "Lista de atividades recuperada com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "funcional": 123456789,
                            "codigo_atividade": 1,
                            "descricao": "Treino de peito",
                            "data_hora": "2026-05-17T14:30:00"
                        },
                        {
                            "funcional": 987654321,
                            "codigo_atividade": 3,
                            "descricao": "Treino funcional",
                            "data_hora": "2026-05-17T20:15:00"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Nenhuma atividade encontrada."
        }
    }
)
def buscar_todas_atividades(
    db: Session = Depends(get_db)
):

    return controller_atividades_realizadas(
        db
    ).buscar_todas_atividades()