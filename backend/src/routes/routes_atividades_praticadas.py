from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.config_banco import get_db


from src.interfaces.schema_atividades import (
    AtividadeCriacaoSchema,
    AtividadeRespostaSchema
)

from src.contollers.atividades_realizadas import controller_atividades_realizadas


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
    summary="Cadastrar atividade",
    description="Cria um novo registro de atividade física."
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

    controller_atividades_realizadas(db).cadastrar_atividade(nova_atividade)

    return nova_atividade




# ==========================================
# Buscar atividades por funcional
# ==========================================

@roteador_atividades_praticadas.get(
    "/{funcional}",
    response_model=List[AtividadeRespostaSchema],
    summary="Buscar atividade por funcional",
    description="Retorna atividades vinculadas a um funcional."
)
def buscar_por_funcional(
    funcional: int,
    db: Session = Depends(get_db)
):

    return controller_atividades_realizadas(db).buscar_por_funcional(funcional)



# ==========================================
# Buscar todas as atividades realizadas
# ==========================================

@roteador_atividades_praticadas.get(
    "/",
    response_model=List[AtividadeRespostaSchema],
    summary="Buscar todas as atividades",
    description="Retorna todas as atividades registradas."
)
def buscar_todas_atividades(
    db: Session = Depends(get_db)
):

    return controller_atividades_realizadas(db).buscar_todas_atividades()