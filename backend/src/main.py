from fastapi import FastAPI

from src.routes.routes_atividade import roteador_atividades as rotas_de_atividades
from src.routes.routes_atividades_praticadas import roteador_atividades_praticadas as rotas_de_atividades_praticadas
from src.models.model_atividade import model_atividades
from src.models.model_atividade_realizada import model_atividades_realizadas

app = FastAPI(
    title="Olympus API",
    description="API para gerenciamento de atividades físicas",
    version="1.0.0"
)

app.include_router(rotas_de_atividades)
app.include_router(rotas_de_atividades_praticadas)