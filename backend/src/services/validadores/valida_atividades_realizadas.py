from fastapi import HTTPException

from src.models.model_atividade import model_atividades


class service_validacao_atividade:


    def validar(
        self,
        payload,
        db
    ):

        if payload.get("funcional") <= 0:

            raise HTTPException(
                status_code=400,
                detail="Funcional inválido."
            )
        
        # ==========================================
        # Validar atividade existente
        # ==========================================
        atividade = db.query(
            model_atividades
        ).filter(
            model_atividades.nome_atividade == payload.get("codigo_atividade")
        ).first()


        if not atividade:

            raise HTTPException(
                status_code=404,
                detail="Atividade informada não existe."
            )


        return atividade
