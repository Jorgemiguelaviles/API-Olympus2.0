from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

PUBLIC_KEY = open(os.getenv("PUBLIC_KEY_PATH")).read()
ALGORITHM = "RS256"


# ==========================================
# ROTAS PÚBLICAS
# ==========================================
PUBLIC_ROUTES = {
    "/usuarios/login",
    "/usuarios/cadastro",
    "/docs",
    "/openapi.json"
}

# normaliza removendo barra final
PUBLIC_ROUTES = {r.rstrip("/") for r in PUBLIC_ROUTES}


# ==========================================
# ROTAS LIBERADAS PARA USER COMUM
# ==========================================
USER_ALLOWED_ROUTES = {
    ("POST", "/atividadespraticadas"),
    ("GET", "/atividades/opcoes"),
}


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # ==========================================
        # NORMALIZAÇÃO
        # ==========================================
        path = request.url.path.rstrip("/")
        if path == "":
            path = "/"

        method = request.method

        route_key = (method, path)

        # ==========================================
        # ROTAS PÚBLICAS
        # ==========================================
        if path in PUBLIC_ROUTES:
            return await call_next(request)

        # ==========================================
        # TOKEN
        # ==========================================
        auth = request.headers.get("Authorization")

        if not auth:
            raise HTTPException(
                status_code=401,
                detail="Token ausente"
            )

        try:
            scheme, token = auth.split(" ")

            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Formato de autenticação inválido"
                )

            payload = jwt.decode(
                token,
                PUBLIC_KEY,
                algorithms=[ALGORITHM]
            )

        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Header Authorization inválido"
            )

        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        # ==========================================
        # USUÁRIO ATIVO
        # ==========================================
        if not payload.get("usuario_ativado", False):
            raise HTTPException(
                status_code=403,
                detail="Usuário desativado"
            )

        # ==========================================
        # SALVA USER NO REQUEST
        # ==========================================
        request.state.user = payload

        # ==========================================
        # ROOT LIBERADO
        # ==========================================
        if payload.get("usuario_root"):
            return await call_next(request)

        # ==========================================
        # USER COMUM
        # ==========================================

        # ROTAS EXATAS
        if route_key in USER_ALLOWED_ROUTES:
            return await call_next(request)

        # GET /atividadespraticadas/{id}
        if (
            method == "GET"
            and path.startswith("/atividadespraticadas/")
        ):
            return await call_next(request)

        # ==========================================
        # BLOQUEIO
        # ==========================================
        raise HTTPException(
            status_code=403,
            detail="Acesso negado para usuário comum"
        )