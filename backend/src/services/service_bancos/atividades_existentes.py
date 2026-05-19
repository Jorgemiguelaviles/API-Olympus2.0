# src/services/service_bancos/atividades.py

from fastapi import HTTPException

from src.models.model_atividades import model_atividades


class service_atividades:

    def __init__(self, db):

        self.db = db

    # ==========================================
    # CADASTRAR ATIVIDADE
    # ==========================================
    def cadastrar_atividade(self, payload: dict):

        try:

            nova_atividade = model_atividades(
                nome_atividade=payload.get("descricao")
            )

            self.db.add(nova_atividade)

            self.db.commit()

            self.db.refresh(nova_atividade)

            return nova_atividade

        except Exception as erro:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao cadastrar atividade: {str(erro)}"
            )

    # ==========================================
    # BUSCAR ATIVIDADES
    # ==========================================
    def buscar_todas_atividades(self):

        return self.db.query(
            model_atividades
        ).all()