from datetime import datetime
from typing import Optional, List

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


# ==========================================
# ATIVIDADE
# ==========================================
class AtividadeResponseSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    funcional: int

    codigo_atividade: str

    nome_atividade: str

    data_hora: datetime


# ==========================================
# TASK IA
# ==========================================
class AnaliseIATaskSchema(BaseModel):

    task_id: str = Field(
        description="ID da task Celery"
    )

    status: str = Field(
        description="Status inicial da task"
    )

    endpoint_consulta: str = Field(
        description="Endpoint para consultar status"
    )


# ==========================================
# RESPONSE GET FUNCIONAL
# ==========================================
class AtividadesPraticadasResponseSchema(
    BaseModel
):

    atividades: List[
        AtividadeResponseSchema
    ]

    analise_ia: AnaliseIATaskSchema


# ==========================================
# POST RESPONSE
# ==========================================
class CadastroAtividadeResponseSchema(
    BaseModel
):

    status: str

    atividade: (
        AtividadeResponseSchema
    )


# ==========================================
# CREATE PAYLOAD
# ==========================================
class AtividadeCriacaoSchema(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "codigo_atividade":
                "SUPINO-001",

                "descricao":
                "Treino de peito"
            }
        }
    )

    codigo_atividade: str = Field(
        ...,
        min_length=1
    )

    descricao: Optional[str] = None