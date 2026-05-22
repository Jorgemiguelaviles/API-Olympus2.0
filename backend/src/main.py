from fastapi import FastAPI
from fastapi.security import HTTPBearer

from src.middlewares.bearer import AuthMiddleware

from src.routes.routes_atividades import (
    roteador_atividades as rotas_de_atividades
)

from src.routes.routes_atividades_realizadas import (
    roteador_atividades_praticadas as rotas_de_atividades_praticadas
)

from src.routes.routes_acessos import (
    roteador_usuarios as rotas_de_usuarios
)

from src.routes.routes_analise_IA import (
    roteador_analise_ia as rotas_de_analise_ia
)

from src.interfaces.docs.docs_main import (
    SWAGGER_CONFIG
)


# ==========================================
# SECURITY
# ==========================================

bearer_scheme = HTTPBearer()


# ==========================================
# APP
# ==========================================

app = FastAPI(
    **SWAGGER_CONFIG
)


# ==========================================
# MIDDLEWARES
# ==========================================

app.add_middleware(AuthMiddleware)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(
    rotas_de_atividades
)

app.include_router(
    rotas_de_atividades_praticadas
)

app.include_router(
    rotas_de_usuarios
)

app.include_router(
    rotas_de_analise_ia
)



print("\n========== ROTAS REGISTRADAS ==========")

for route in app.routes:
    print(route.path)

print("=======================================\n")