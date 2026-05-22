from typing import Optional, Any

from pydantic import (
    BaseModel,
    Field
)


# ==========================================
# STATUS ANALISE IA
# ==========================================
class StatusAnaliseIAResponseSchema(BaseModel):

    status: str = Field(
        description=(
            "Status atual da análise "
            "(processando/concluido/erro)"
        )
    )

    resultado: Optional[Any] = Field(
        default=None,
        description="Resultado final da análise IA"
    )

    erro: Optional[str] = Field(
        default=None,
        description="Mensagem de erro da análise"
    )