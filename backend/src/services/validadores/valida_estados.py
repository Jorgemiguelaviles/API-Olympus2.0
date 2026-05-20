from fastapi import HTTPException

from src.models.model_usuarios import (
    model_usuarios
)


class service_validacao_estados:

    # ==========================================
    # CAMPOS PERMITIDOS
    # ==========================================
    CAMPOS_PERMITIDOS = [
        "usuario_root",
        "usuario_ativado"
    ]

    # ==========================================
    # VALIDAR ALTERAÇÃO CONFIG
    # ==========================================
    def validar(
        self,
        funcional: int,
        campo: str,
        db
    ):

        # ==========================================
        # VALIDAR USUÁRIO
        # ==========================================
        usuario = db.query(
            model_usuarios
        ).filter(
            model_usuarios.funcional == funcional
        ).first()

        if not usuario:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        # ==========================================
        # VALIDAR CAMPO
        # ==========================================
        if campo not in self.CAMPOS_PERMITIDOS:

            raise HTTPException(
                status_code=400,
                detail="Campo inválido para alteração."
            )

        return usuario