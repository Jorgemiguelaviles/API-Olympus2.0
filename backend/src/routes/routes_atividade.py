from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from src.config.config_banco import get_db


from src.interfaces.schema_atividades import (
    AtividadeCriacaoSchema,
    AtividadeRespostaSchema
)
from src.contollers.atividades_existentes import controller_atividade_existente



roteador = APIRouter(
    prefix="/atividades",
    tags=["Atividades"]
)


# ==========================================
# Mock temporário para o case
# ==========================================

banco_falso = [
    {
        "funcional": 123,
        "codigo_atividade": "RUN",
        "descricao": "Corrida de 5km",
        "data_hora": datetime.now()
    },
    {
        "funcional": 123,
        "codigo_atividade": "SWIM",
        "descricao": "Natação de 30 minutos",
        "data_hora": datetime.now()
    },
    {
        "funcional": 456,
        "codigo_atividade": "CYCL",
        "descricao": "Ciclismo de 10km",
        "data_hora": datetime.now()
    }
]


# Atividades disponíveis no sistema
banco_atividades_existentes = [
    "RUN",
    "SWIM",
    "CYCL",
    "WALK",
    "YOGA"
]


# ==========================================
# Cadastro de atividade realizada
# ==========================================

@roteador.post(
    "/",
    response_model=AtividadeRespostaSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar atividade",
    description="Cria um novo registro de atividade física."
)
def cadastrar_atividade(
    payload: AtividadeCriacaoSchema
):

    nova_atividade = {
        "funcional": payload.funcional,
        "codigo_atividade": payload.codigo_atividade,
        "descricao": payload.descricao,
        "data_hora": datetime.now()
    }

    banco_falso.append(
        nova_atividade
    )

    return nova_atividade


# ==========================================
# Buscar todas as atividades realizadas
# ==========================================

@roteador.get(
    "/",
    response_model=List[AtividadeRespostaSchema],
    summary="Buscar todas as atividades",
    description="Retorna todas as atividades registradas."
)
def buscar_todas_atividades():

    return banco_falso


# ==========================================
# Buscar opções de atividades disponíveis
# ==========================================

@roteador.get(
    "/opcoes",
    summary="Buscar atividades disponíveis",
    description="Retorna as atividades disponíveis para seleção."
)
def buscar_opcoes_atividades(
    db: Session = Depends(get_db)
):

    return controller_atividade_existente(db).get_all_activities()


# ==========================================
# Buscar atividades por funcional
# ==========================================

@roteador.get(
    "/{funcional}",
    response_model=List[AtividadeRespostaSchema],
    summary="Buscar atividade por funcional",
    description="Retorna atividades vinculadas a um funcional."
)
def buscar_por_funcional(
    funcional: int
):

    return [
        atividade
        for atividade in banco_falso
        if atividade["funcional"] == funcional
    ]