from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from src.config.config_banco import get_db


from src.interfaces.schema_atividades import (
    AtividadeExistenteResponseSchema
)
from src.contollers.atividades_existentes import controller_atividade_existente



roteador_atividades = APIRouter(
    prefix="/atividades",
    tags=["Atividades"]
)




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

    return controller_atividade_existente(db).gerencia_atividades()

