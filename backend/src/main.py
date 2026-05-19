from fastapi import FastAPI

from src.routes.routes_atividades import roteador_atividades as rotas_de_atividades
from src.routes.routes_atividades_realizadas import roteador_atividades_praticadas as rotas_de_atividades_praticadas
from src.routes.routes_acessos import roteador_usuarios as rotas_de_usuarios
from src.models.model_atividades import model_atividades
from src.models.model_atividades_realizadas import model_atividades_realizadas
from src.models.model_usuarios import model_usuarios




app = FastAPI(
    title="Olympus API",
    description="API para gerenciamento de atividades físicas",
    version="1.0.0"
)

app.include_router(rotas_de_atividades)
app.include_router(rotas_de_atividades_praticadas)
app.include_router(rotas_de_usuarios)