import re

from fastapi import HTTPException

from src.models.model_atividades import model_atividades


class service_validacao_atividade:

    def validar(
        self,
        payload,
        db
    ):

        funcional = str(
            payload.get("funcional")
        )

        # ==========================================
        # Validar funcional (9 dígitos)
        # ==========================================
        if not re.fullmatch(
            r"\d{9}",
            funcional
        ):

            raise HTTPException(
                status_code=400,
                detail="Funcional deve conter exatamente 9 números."
            )

        # ==========================================
        # Validar atividade existente
        # ==========================================
        atividade = db.query(
            model_atividades
        ).filter(
            model_atividades.nome_atividade == payload.get(
                "codigo_atividade"
            )
        ).first()

        if not atividade:

            raise HTTPException(
                status_code=404,
                detail="Atividade informada não existe."
            )

        return atividade