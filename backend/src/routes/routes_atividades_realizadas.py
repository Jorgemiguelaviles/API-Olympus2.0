from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Request
)

from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.schemas.schema_atividaddes_realizadas import (
    AtividadeCriacaoSchema
)

from src.interfaces.docs.docs_atividades_realizadas import (
    DOC_CADASTRAR_ATIVIDADE,
    DOC_BUSCAR_POR_FUNCIONAL,
    DOC_BUSCAR_TODAS
)

from src.contollers.controller_atividades_realizadas import (
    controller_atividades_realizadas
)


# ==========================================
# ROUTER
# ==========================================
roteador_atividades_praticadas = APIRouter(
    prefix="/atividadespraticadas",
    tags=["📊 Atividades Praticadas"]
)


# ==========================================
# DEPENDENCY
# ==========================================
def get_controller(
    db: Session = Depends(get_db)
):
    return controller_atividades_realizadas(db)


# ==========================================
# CADASTRAR ATIVIDADE
# ==========================================
@roteador_atividades_praticadas.post(
    "/",
    **DOC_CADASTRAR_ATIVIDADE
)
def cadastrar_atividade(
    payload: AtividadeCriacaoSchema,
    request: Request,
    controller = Depends(get_controller)
):

    user = request.state.user

    nova_atividade = {
        "funcional": user["funcional"],
        "codigo_atividade": payload.codigo_atividade,
        "descricao": payload.descricao,
        "data_hora": datetime.now()
    }

    return controller.cadastrar_atividade(
        nova_atividade
    )


# ==========================================
# BUSCAR MINHAS ATIVIDADES
# ==========================================
@roteador_atividades_praticadas.get(
    "/minhas",
    **DOC_BUSCAR_POR_FUNCIONAL
)
def buscar_minhas_atividades(
    request: Request,
    controller = Depends(get_controller)
):

    user = request.state.user

    return controller.buscar_por_funcional(
        user["funcional"]
    )


# ==========================================
# BUSCAR TODAS
# ==========================================
@roteador_atividades_praticadas.get(
    "/",
    **DOC_BUSCAR_TODAS
)
def buscar_todas_atividades(
    controller = Depends(get_controller)
):

    return controller.buscar_todas_atividades()