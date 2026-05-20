from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.schemas.schema_atividades import (
    AtividadeCriacaoOpcaoSchema
)

from src.interfaces.docs.docs_atividades import (
    DOC_BUSCAR_OPCOES_ATIVIDADES,
    DOC_CADASTRAR_OPCAO_ATIVIDADE
)

from src.contollers.controller_atividades import (
    controller_atividade_existente
)


roteador_atividades = APIRouter(
    prefix="/atividades",
    tags=["🏋️ Atividades"]
)


# ==========================================
# BUSCAR OPÇÕES
# ==========================================
@roteador_atividades.get(
    "/opcoes",
    **DOC_BUSCAR_OPCOES_ATIVIDADES
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
    status_code=status.HTTP_201_CREATED,
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