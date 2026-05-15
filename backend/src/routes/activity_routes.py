from fastapi import APIRouter, status
from typing import List

from src.interfaces.activity_schema import (
    ActivityCreateSchema,
    ActivityResponseSchema
)

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


# Mock temporário até conectar service/repository
fake_db = []


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

    fake_db.append(activity)

    return activity


@router.get(
    "/",
    response_model=List[ActivityResponseSchema],
    summary="Listar todas as atividades",
    description="Retorna todas as atividades registradas."
)
def get_all_activities():

    return fake_db


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