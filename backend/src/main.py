from fastapi import FastAPI

from src.routes.routes_atividade import roteador_atividades as rotas_de_atividades
from backend.src.routes.routes_atividades_realizadas import roteador_atividades_praticadas as rotas_de_atividades_praticadas
from src.models.model_atividade import model_atividades
from backend.src.models.model_atividade_realizadas import model_atividades_realizadas

app = FastAPI(
    title="Olympus API",
    description="API para gerenciamento de atividades físicas",
    version="1.0.0"
)

app.include_router(rotas_de_atividades)
app.include_router(rotas_de_atividades_praticadas)