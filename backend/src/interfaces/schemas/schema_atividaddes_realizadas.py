from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


# ==========================================
# ATIVIDADE RESPONSE
# ==========================================
class AtividadeResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    funcional: int = Field(
        description="Funcional do usuário"
    )

    codigo_atividade: str = Field(
        description="Código identificador da atividade"
    )

    nome_atividade: str = Field(
        description="Nome ou descrição da atividade"
    )

    data_hora: datetime = Field(
        description="Data e horário da atividade"
    )


# ==========================================
# IA RESPONSE
# ==========================================
class AnaliseIAResponseSchema(BaseModel):

    model_config = ConfigDict(extra="ignore")

    status: str = Field(
        description="Status da análise"
    )

    mensagem: Optional[str] = Field(
        default=None,
        description="Mensagem complementar"
    )

    resumo: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Resumo estatístico das atividades"
    )

    analise: Optional[str] = Field(
        default=None,
        description="Análise textual gerada pela IA"
    )


# ==========================================
# GET /MINHAS RESPONSE
# ==========================================
class AtividadesPraticadasResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    atividades: List[AtividadeResponseSchema]

    analise_ia: AnaliseIAResponseSchema


# ==========================================
# POST RESPONSE
# ==========================================
class CadastroAtividadeResponseSchema(BaseModel):

    status: str

    atividade: AtividadeResponseSchema


# ==========================================
# CREATE PAYLOAD
# ==========================================
class AtividadeCriacaoSchema(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "codigo_atividade": "SUPINO-001",
                "descricao": "Treino de peito e tríceps"
            }
        }
    )

    codigo_atividade: str = Field(
        ...,
        min_length=1,
        description="Código identificador da atividade"
    )

    descricao: Optional[str] = Field(
        default=None,
        description="Descrição detalhada da atividade"
    )