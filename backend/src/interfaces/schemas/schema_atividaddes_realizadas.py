# src/interfaces/schemas/schema_atividades.py

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# ==========================================
# Payload de criação
# ==========================================

class AtividadeCriacaoSchema(BaseModel):

    funcional: int = Field(
        ...,
        example=123456789,
        description="Código funcional do usuário"
    )

    codigo_atividade: str = Field(
        ...,
        example="RUN",
        description="Código da atividade"
    )

    descricao: Optional[str] = Field(
        None,
        example="Corrida de 5km"
    )