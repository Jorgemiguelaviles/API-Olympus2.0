# src/services/service_seguranca/service_login.py

from fastapi import HTTPException
from passlib.context import CryptContext

from src.models.model_usuarios import model_usuarios


class service_login:

    def __init__(self, db):

        self.db = db

        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
            )
    # ==========================================
    # AUTENTICAR USUÁRIO
    # ==========================================
    def autenticar(self, usuario: str, senha: str):

        user = self.db.query(model_usuarios)\
            .filter(model_usuarios.usuario == usuario)\
            .first()

        # ==========================================
        # USUÁRIO NÃO EXISTE
        # ==========================================
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos."
            )

        # ==========================================
        # USUÁRIO DESATIVADO
        # ==========================================
        if not user.usuario_ativado:
            raise HTTPException(
                status_code=403,
                detail="Usuário desativado. Entre em contato com o suporte."
            )

        # ==========================================
        # VERIFICA SENHA
        # ==========================================
        if not self.pwd_context.verify(senha, user.senha_hash):
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos."
            )

        # ==========================================
        # RETORNO CONTROLADO (IMPORTANTE)
        # ==========================================
        return {
            "funcional": user.funcional,
            "usuario": user.usuario,
            "nome": user.nome,
            "usuario_root": user.usuario_root,
            "usuario_ativado": user.usuario_ativado
        }