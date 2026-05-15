from fastapi import FastAPI

from src.routes.routes_atividade import router as activity_router

app = FastAPI(
    title="Olympus API",
    description="API para gerenciamento de atividades físicas",
    version="1.0.0"
)

app.include_router(activity_router)