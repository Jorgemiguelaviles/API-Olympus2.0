from fastapi import HTTPException
from passlib.context import CryptContext

from src.services.validadores.valida_atualizacao_usuario import service_validacao_atualizacao_usuario
from src.services.validadores.valida_estados import service_validacao_estados
from src.services.validadores.valida_usuarios import (
    service_validacao_usuario
)

from src.services.service_bancos.usuarios import (
    service_usuarios
)

from src.services.service_bancos.login import (
    service_login
)

from src.services.service_seguranca.limite_login import (
    brute_force_instance
)

from src.services.service_seguranca.jwt import (
    create_access_token
)


class controller_usuarios:

    # ==========================================
    # CONSTRUTOR
    # ==========================================
    def __init__(self, db):

        self.db = db

        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

        # SERVICES
        self.usuario_service = service_usuarios(db)

        self.login_service = service_login(db)

        self.brute_force = brute_force_instance

    # ==========================================
    # CADASTRAR USUÁRIO
    # ==========================================
    def cadastrar_usuario(self, payload):

        try:

            # validação
            service_validacao_usuario().validar(
                payload,
                self.db
            )

            # hash senha
            senha_hash = self.pwd_context.hash(
                payload.get("senha")
            )

            novo_usuario = {
                "usuario": payload.get("usuario"),
                "senha_hash": senha_hash,
                "nome": payload.get("nome")
            }

            return self.usuario_service.salvar(
                novo_usuario
            )

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao cadastrar usuário: {str(erro)}"
            )

    # ==========================================
    # LISTAR USUÁRIOS
    # ==========================================
    def listar_usuarios(self, page: int):

        try:

            return self.usuario_service.listar_usuarios(
                page
            )

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao listar usuários: {str(erro)}"
            )

    # ==========================================
    # LOGIN
    # ==========================================
    def login(self, payload):

        usuario = payload.get("usuario")
        senha = payload.get("senha")

        try:

            # brute force
            self.brute_force.verificar_bloqueio(
                usuario
            )

            # autenticação
            user = self.login_service.autenticar(
                usuario,
                senha
            )

            # reset brute force
            self.brute_force.reset(
                usuario
            )

            # token
            token = create_access_token({
                "sub": str(user["funcional"]),
                "funcional": user["funcional"],
                "usuario": user["usuario"],
                "nome": user["nome"],
                "usuario_root": user["usuario_root"],
                "usuario_ativado": user["usuario_ativado"]
            })

            return {
                "access_token": token,
                "token_type": "bearer"
            }

        except HTTPException as e:

            self.brute_force.registrar_falha(
                usuario
            )

            raise e

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno no login: {str(erro)}"
            )
    # ==========================================
    # ALTERAR CONFIGURAÇÃO USUÁRIO
    # ==========================================
    def alterar_configuracao_usuario(
        self,
        funcional: int,
        campo: str
    ):

        try:

            # valida tudo
            service_validacao_estados().validar(
                funcional,
                campo,
                self.db
            )

            # update
            return self.usuario_service.alterar_configuracao_usuario(
                funcional,
                campo
            )

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao alterar configuração do usuário: {str(erro)}"
            )
            
    # ==========================================
    # ATUALIZAR USUÁRIO
    # ==========================================
    def atualizar_usuario(
        self,
        funcional: int,
        payload
    ):

        try:

            # valida dados atualização
            dados_atualizacao = (
                service_validacao_atualizacao_usuario().validar_atualizacoes(
                    payload,
                    self.db
                )
            )

            # hash senha
            if "senha" in dados_atualizacao:

                dados_atualizacao["senha_hash"] = (
                    self.pwd_context.hash(
                        dados_atualizacao["senha"]
                    )
                )

                del dados_atualizacao["senha"]

            return self.usuario_service.atualizar_usuario(
                funcional,
                dados_atualizacao
            )

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao atualizar usuário: {str(erro)}"
            )