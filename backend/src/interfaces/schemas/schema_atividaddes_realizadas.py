from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# Atividade individual (response)
# ==========================================
class AtividadeResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    funcional: int

    codigo_atividade: str

    nome_atividade: str

    data_hora: datetime


# ==========================================
# IA response
# ==========================================
class AnaliseIAResponseSchema(BaseModel):

    model_config = ConfigDict(extra="ignore")

    status: str

    mensagem: Optional[str] = None

    resumo: Optional[Dict[str, Any]] = None

    analise: Optional[str] = None


# ==========================================
# GET /minhas response
# ==========================================
class AtividadesPraticadasResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    atividades: List[AtividadeResponseSchema]

    analise_ia: AnaliseIAResponseSchema


# ==========================================
# POST response
# ==========================================
class CadastroAtividadeResponseSchema(BaseModel):

    status: str

    atividade: AtividadeResponseSchema


# ==========================================
# CREATE payload
# ==========================================
class AtividadeCriacaoSchema(BaseModel):

    codigo_atividade: str = Field(..., min_length=1)

    descricao: Optional[str] = None