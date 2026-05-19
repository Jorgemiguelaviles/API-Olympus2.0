from fastapi import FastAPI

from src.routes.routes_atividades import roteador_atividades as rotas_de_atividades
from src.routes.routes_atividades_realizadas import roteador_atividades_praticadas as rotas_de_atividades_praticadas
from src.routes.routes_acessos import roteador_usuarios as rotas_de_usuarios

from src.middlewares.bearer import AuthMiddleware


# ==========================================
# TAGS DO SWAGGER
# ==========================================
tags_metadata = [
    {
        "name": "Usuários",
        "description": "Operações relacionadas a cadastro, autenticação e listagem de usuários."
    },
    {
        "name": "Atividades",
        "description": "Gestão de atividades físicas disponíveis no sistema."
    },
    {
        "name": "Atividades Praticadas",
        "description": "Registro e consulta de atividades realizadas pelos usuários."
    }
]


app = FastAPI(
    title="Olympus API",
    description=(
        "API para gerenciamento de atividades físicas e controle de usuários.\n\n"
        "Sistema com autenticação JWT, controle de acesso por usuário root e proteção contra brute force."
    ),
    version="1.0.0",

    # ==========================================
    # SWAGGER CONFIG
    # ==========================================
    openapi_tags=tags_metadata,

    contact={
        "name": "Olympus Support",
        "email": "suporte@olympus.api"
    },

    license_info={
        "name": "Proprietary",
    }
)

# ==========================================
# MIDDLEWARE
# ==========================================
app.add_middleware(AuthMiddleware)

# ==========================================
# ROUTERS
# ==========================================
app.include_router(rotas_de_atividades)
app.include_router(rotas_de_atividades_praticadas)
app.include_router(rotas_de_usuarios)