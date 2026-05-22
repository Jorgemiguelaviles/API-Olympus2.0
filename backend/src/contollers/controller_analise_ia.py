from fastapi import HTTPException

from celery.result import AsyncResult

from src.infraestructure.celery.celery_app import (
    celery_app
)


class controller_analise_ia:


    # ==========================================
    # BUSCAR STATUS DA TASK
    # ==========================================
    def buscar_status_analise(
        self,
        task_id: str
    ):

        try:

            task = AsyncResult(
                task_id,
                app=celery_app
            )

            if task.state == "PENDING":

                return {
                    "status": "processando",
                    "resultado": None,
                    "erro": None
                }

            if task.state == "SUCCESS":

                return {
                    "status": "concluido",
                    "resultado": task.result,
                    "erro": None
                }

            if task.state == "FAILURE":

                return {
                    "status": "erro",
                    "resultado": None,
                    "erro": str(task.result)
                }

            return {
                "status": task.state,
                "resultado": None,
                "erro": None
            }

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=str(erro)
            )