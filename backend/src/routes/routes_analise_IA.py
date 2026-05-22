from fastapi import APIRouter

from src.interfaces.docs.docs_analise_ia import (
    DOC_STATUS_ANALISE_IA
)

from src.contollers.controller_analise_ia import (
    controller_analise_ia
)


roteador_analise_ia = APIRouter(
    prefix="/analise-ia",
    tags=["Análise IA"]
)


# ==========================================
# CONSULTAR STATUS DA ANÁLISE
# ==========================================
@roteador_analise_ia.get(
    "/analise/{task_id}",
    **DOC_STATUS_ANALISE_IA
)
def buscar_status_analise(
    task_id: str
):

    controller = (
        controller_analise_ia()
    )

    return controller.buscar_status_analise(
        task_id
    )
