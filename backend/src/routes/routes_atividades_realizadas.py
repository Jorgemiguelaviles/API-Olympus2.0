# src/routes/routes_atividades.py

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.schemas.schema_atividades import (
    AtividadeCriacaoSchema
)

from src.interfaces.docs.docs_atividades import (
    DOC_CADASTRAR_ATIVIDADE,
    DOC_BUSCAR_POR_FUNCIONAL,
    DOC_BUSCAR_TODAS
)

from src.contollers.atividades_realizadas import (
    controller_atividades_realizadas
)


roteador_atividades_praticadas = APIRouter(
    prefix="/atividades/praticadas",
    tags=["Atividades Praticadas"]
)


# ==========================================
# Cadastro
# ==========================================

@roteador_atividades_praticadas.post(
    "/",
    **DOC_CADASTRAR_ATIVIDADE
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
# Buscar por funcional
# ==========================================

@roteador_atividades_praticadas.get(
    "/{funcional}",
    **DOC_BUSCAR_POR_FUNCIONAL
)
def buscar_por_funcional(
    funcional: int,
    db: Session = Depends(get_db)
):

    return controller_atividades_realizadas(
        db
    ).buscar_por_funcional(
        funcional
    )


# ==========================================
# Buscar todas
# ==========================================

@roteador_atividades_praticadas.get(
    "/",
    **DOC_BUSCAR_TODAS
)
def buscar_todas_atividades(
    db: Session = Depends(get_db)
):

    return controller_atividades_realizadas(
        db
    ).buscar_todas_atividades()