from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.docs.docs_atividades import (
    DOC_CADASTRAR_OPCAO_ATIVIDADE
)

from src.interfaces.schemas.schema_atividades import (
    AtividadeCriacaoOpcaoSchema,
    AtividadeExistenteResponseSchema
)

from src.contollers.controller_atividades import (
    controller_atividade_existente
)

roteador_atividades = APIRouter(
    prefix="/atividades",
    tags=["Atividades"]
)


# ==========================================
# BUSCAR OPÇÕES
# ==========================================
@roteador_atividades.get(
    "/opcoes",
    response_model=List[AtividadeExistenteResponseSchema],
    summary="Buscar atividades disponíveis",
    description="Retorna as atividades disponíveis para seleção.",
    responses={
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
)
def buscar_opcoes_atividades(
    db: Session = Depends(get_db)
):

    return controller_atividade_existente(
        db
    ).busca_atividades()


# ==========================================
# CADASTRAR OPÇÃO
# ==========================================
@roteador_atividades.post(
    "/opcoes",
    status_code=201,
    **DOC_CADASTRAR_OPCAO_ATIVIDADE
)
def cadastrar_opcao_atividade(
    payload: AtividadeCriacaoOpcaoSchema,
    db: Session = Depends(get_db)
):

    nova_atividade = {
        "descricao": payload.descricao
    }

    return controller_atividade_existente(
        db
    ).cadastrar_atividade(
        nova_atividade
    )