from fastapi import HTTPException
from passlib.context import CryptContext

from src.services.validadores.valida_usuarios import service_validacao_usuario
from src.services.service_bancos.usuarios import service_usuarios
from src.services.service_bancos.login import service_login
from src.services.service_seguranca.limite_login import brute_force_instance
from src.services.service_seguranca.jwt import create_access_token


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

        # 🔥 IMPORTANTE: singleton global
        self.brute_force = brute_force_instance

    # ==========================================
    # CADASTRO
    # ==========================================
    def cadastrar_usuario(self, payload):

        try:

            service_validacao_usuario().validar(payload, self.db)

            senha_hash = self.pwd_context.hash(payload.get("senha"))

            novo_usuario = {
                "usuario": payload.get("usuario"),
                "senha_hash": senha_hash,
                "nome": payload.get("nome")
            }

            return self.usuario_service.salvar(novo_usuario)

        except HTTPException:
            raise

        except Exception as erro:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao cadastrar usuário: {str(erro)}"
            )

    # ==========================================
    # LISTAGEM
    # ==========================================
    def listar_usuarios(self, page: int):

        try:
            return self.usuario_service.listar_usuarios(page)

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

            # 1. CHECK BRUTE FORCE
            self.brute_force.verificar_bloqueio(usuario)

            # 2. AUTH
            user = self.login_service.autenticar(usuario, senha)

            # 3. RESET BRUTE FORCE (login ok)
            self.brute_force.reset(usuario)

            # 4. TOKEN
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

            # registra falha
            self.brute_force.registrar_falha(usuario)
            raise e

        except Exception as erro:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno no login: {str(erro)}"
            )