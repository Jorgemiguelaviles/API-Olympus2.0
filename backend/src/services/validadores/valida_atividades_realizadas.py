from fastapi import HTTPException


class service_validacao_atividade:


    def validar(
        self,
        payload
    ):

        if payload.get("funcional") <= 0:

            raise HTTPException(
                status_code=400,
                detail="Funcional inválido."
            )
