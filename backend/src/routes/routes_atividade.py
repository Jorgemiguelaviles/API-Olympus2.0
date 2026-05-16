from fastapi import APIRouter, status
from typing import List

from src.interfaces.schema_atividades import (
    ActivityCreateSchema,
    ActivityResponseSchema
)

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


# Mock temporário até conectar service/repository
banco_falso = {
        "funcional": 123,
        "codigo_atividade": "RUN",
        "descricao": "Corrida de 5km",
        "data_hora": __import__("datetime").datetime.now()
    },{
        "funcional": 123,
        "codigo_atividade": "SWIM",
        "descricao": "Natação de 30 minutos",
        "data_hora": __import__("datetime").datetime.now()
    },{
        "funcional": 456,
        "codigo_atividade": "CYCL",
        "descricao": "Ciclismo de 10km",
        "data_hora": __import__("datetime").datetime.now()
    }




@router.post(
    "/",
    response_model=ActivityResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma atividade realizada",
    description="Cria um novo registro de atividade física."
)
def create_activity(payload: ActivityCreateSchema):

    activity = {
        "funcional": payload.funcional,
        "codigo_atividade": payload.codigo_atividade,
        "descricao": payload.descricao,
        "data_hora": __import__("datetime").datetime.now()
    }

    banco_falso.append(activity)

    return activity


@router.get(
    "/",
    response_model=List[ActivityResponseSchema],
    summary="Listar todas as atividades",
    description="Retorna todas as atividades registradas."
)
def get_all_activities():

    return banco_falso

@router.get(
    "/opcoesAtividades",
    response_model=List[ActivityResponseSchema],
    summary="Listar todas as atividades",
    description="Retorna todas as atividades registradas."
)
def get_all_activities():

    return banco_atividades_existentes


@router.get(
    "/{funcional}",
    response_model=List[ActivityResponseSchema],
    summary="Buscar atividades por funcional",
    description="Retorna atividades registradas de um usuário específico."
)
def get_activity_by_funcional(funcional: int):

    return [
        activity
        for activity in fake_db
        if activity["funcional"] == funcional
    ]