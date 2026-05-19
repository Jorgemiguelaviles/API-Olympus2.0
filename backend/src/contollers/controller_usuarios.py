# src/controllers/controller_usuarios.py

from fastapi import HTTPException
from passlib.context import CryptContext

from src.services.validadores.valida_usuarios import (
    service_validacao_usuario
)

from src.services.service_bancos.usuarios import (
    service_usuarios
)


class controller_usuarios:

    # ==========================================
    # Construtor
    # ==========================================
    def __init__(self, db):

        self.db = db

        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )


    # ==========================================
    # Cadastro de usuário
    # ==========================================
    def cadastrar_usuario(
        self,
        payload
    ):

        try:

            # ==========================================
            # Validar dados
            # ==========================================
            service_validacao_usuario().validar(
                payload,
                self.db
            )

            print(payload.get("senha"))

            # ==========================================
            # Gerar hash da senha
            # ==========================================
            senha_hash = self.pwd_context.hash(
                payload.get("senha")
            )

            # ==========================================
            # Payload final
            # ==========================================
            novo_usuario = {
                "usuario": payload.get("usuario"),
                "senha_hash": senha_hash,
                "nome": payload.get("nome")
            }

            print(f"Payload final para cadastro: {novo_usuario}")

            # ==========================================
            # Salvar usuário
            # ==========================================
            usuario_salvo = service_usuarios(
                self.db
            ).salvar(
                novo_usuario
            )

            return usuario_salvo

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao cadastrar usuário: {str(erro)}"
            )
        

    def listar_usuarios(self, page: int):

        try:

            service = service_usuarios(self.db)

            return service.listar_usuarios(page)

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao listar usuários: {str(erro)}"
            )