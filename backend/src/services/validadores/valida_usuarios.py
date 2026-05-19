import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.model_usuarios import model_usuarios


class service_validacao_usuario:

    # ==========================================
    # Validar cadastro
    # ==========================================
    def validar(
        self,
        payload: dict,
        db: Session
    ):

        usuario = payload.get("usuario")
        senha = payload.get("senha")
        nome = payload.get("nome")

        # ==========================================
        # Campos obrigatórios
        # ==========================================
        if not usuario or not usuario.strip():

            raise HTTPException(
                status_code=400,
                detail="O campo usuário é obrigatório."
            )

        if not senha or not senha.strip():

            raise HTTPException(
                status_code=400,
                detail="O campo senha é obrigatório."
            )

        if not nome or not nome.strip():

            raise HTTPException(
                status_code=400,
                detail="O campo nome é obrigatório."
            )

        # ==========================================
        # Validar formato de email
        # ==========================================
        regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(regex_email, usuario):

            raise HTTPException(
                status_code=400,
                detail="Formato de email inválido."
            )

        # ==========================================
        # Validar senha forte
        # ==========================================
        regex_senha_forte = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'

        if not re.match(regex_senha_forte, senha):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Senha fraca. A senha deve conter no mínimo 8 caracteres, "
                    "incluindo letra maiúscula, minúscula, número e caractere especial."
                )
            )

        # ==========================================
        # Verificar usuário existente
        # ==========================================
        usuario_existente = db.query(
            model_usuarios
        ).filter(
            model_usuarios.usuario == usuario
        ).first()

        if usuario_existente:

            raise HTTPException(
                status_code=409,
                detail="Usuário já cadastrado."
            )