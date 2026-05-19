# src/services/validadores/service_validacao_atividade.py

from fastapi import HTTPException

from src.models.model_atividades import model_atividades


class service_validacao_atividade:

    # ==========================================
    # VALIDAR CADASTRO DE ATIVIDADE
    # ==========================================
    def validar_cadastro(
        self,
        payload: dict,
        db
    ):

        descricao = payload.get("descricao")

        # ==========================================
        # CAMPO OBRIGATÓRIO
        # ==========================================
        if not descricao or not descricao.strip():

            raise HTTPException(
                status_code=400,
                detail="A descrição da atividade é obrigatória."
            )

        descricao = descricao.strip().upper()

        # ==========================================
        # TAMANHO MÍNIMO
        # ==========================================
        if len(descricao) < 3:

            raise HTTPException(
                status_code=400,
                detail="A atividade deve possuir ao menos 3 caracteres."
            )

        # ==========================================
        # VALIDAR DUPLICIDADE
        # ==========================================
        atividade_existente = db.query(
            model_atividades
        ).filter(
            model_atividades.nome_atividade == descricao
        ).first()

        if atividade_existente:

            raise HTTPException(
                status_code=409,
                detail="Essa atividade já está cadastrada."
            )

        # ==========================================
        # RETORNO PADRONIZADO
        # ==========================================
        return {
            "descricao": descricao
        }