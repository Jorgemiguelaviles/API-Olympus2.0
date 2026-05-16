from fastapi import HTTPException
from src.services.service_bancos.atividaes_realizadas import (
    service_atividades )


class controller_atividade_existente:

    def __init__(self, db):
        self.db = db


    def gerencia_atividades(self):

        try:

            service = service_atividades(
                self.db
            )

            atividades = service.buscar_todas_atividades()

            if not atividades:

                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada."
                )

            return atividades

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao consultar atividades: {str(erro)}"
            )